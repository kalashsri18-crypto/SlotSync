import os, sqlite3
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template_string

app=Flask(__name__); app.config["DATABASE"]=os.environ.get("DATABASE","slotsync.sqlite3")
def db():
 c=sqlite3.connect(app.config["DATABASE"]); c.row_factory=sqlite3.Row; return c
def init_db():
 with db() as c:
  c.execute("""CREATE TABLE IF NOT EXISTS appointments(id INTEGER PRIMARY KEY, customer TEXT NOT NULL, service TEXT NOT NULL, starts_at TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'booked', ticket INTEGER NOT NULL, UNIQUE(starts_at,ticket))""")
  c.execute("CREATE INDEX IF NOT EXISTS idx_slots ON appointments(starts_at,status)")
@app.get("/api/slots")
def slots():
 day=request.args.get("date",datetime.now().date().isoformat())
 with db() as c: rows=c.execute("SELECT * FROM appointments WHERE substr(starts_at,1,10)=? ORDER BY starts_at,ticket",(day,)).fetchall()
 return jsonify([dict(x) for x in rows])
@app.post("/api/appointments")
def book():
 d=request.get_json(silent=True) or request.form
 try:
  customer=str(d.get("customer","")).strip(); service=str(d.get("service","")).strip()
  start=datetime.fromisoformat(str(d.get("starts_at","")))
  if not customer or not service or start<=datetime.now(): raise ValueError()
 except (ValueError,TypeError): return jsonify(error="Provide customer, service and a future ISO date/time."),400
 with db() as c:
  count=c.execute("SELECT COUNT(*) n FROM appointments WHERE starts_at=? AND status='booked'",(start.isoformat(timespec="minutes"),)).fetchone()["n"]
  if count>=3: return jsonify(error="This slot is full (capacity: 3)."),409
  ticket=c.execute("SELECT COALESCE(MAX(ticket),0)+1 n FROM appointments WHERE substr(starts_at,1,10)=?",(start.date().isoformat(),)).fetchone()["n"]
  cur=c.execute("INSERT INTO appointments(customer,service,starts_at,ticket) VALUES(?,?,?,?)",(customer,service,start.isoformat(timespec="minutes"),ticket))
  row=c.execute("SELECT * FROM appointments WHERE id=?",(cur.lastrowid,)).fetchone()
 return jsonify(dict(row)),201
@app.patch("/api/appointments/<int:item_id>/cancel")
def cancel(item_id):
 with db() as c:
  cur=c.execute("UPDATE appointments SET status='cancelled' WHERE id=? AND status='booked'",(item_id,))
 return (jsonify(status="cancelled"),200) if cur.rowcount else (jsonify(error="Active appointment not found."),404)
@app.get("/api/queue")
def queue():
 start=request.args.get("starts_at","")
 with db() as c: rows=c.execute("SELECT ticket,customer,service FROM appointments WHERE starts_at=? AND status='booked' ORDER BY ticket",(start,)).fetchall()
 return jsonify([dict(x,position=i+1) for i,x in enumerate(rows)])
@app.get("/")
def home():
 return render_template_string("""<!doctype html><title>SlotSync</title><meta name=viewport content="width=device-width,initial-scale=1"><style>body{font:16px system-ui;max-width:800px;margin:3rem auto;padding:0 1rem;background:#f5f7fb;color:#182238}main{background:white;padding:2rem;border-radius:16px}form{display:flex;gap:.6rem;flex-wrap:wrap}input,button{padding:.7rem;border:1px solid #ccd3df;border-radius:8px}button{background:#245b62;color:white}li{padding:.6rem;border-bottom:1px solid #eee}</style><main><h1>SlotSync</h1><p>Appointments and walk-in queue. Each time slot holds up to three bookings.</p><form id=f><input name=customer placeholder=Customer required><input name=service placeholder=Service required><input name=starts_at type=datetime-local required><button>Book slot</button></form><h2>Bookings</h2><ul id=list></ul></main><script>async function load(){let a=await(await fetch('/api/slots')).json();list.innerHTML=a.map(x=>'<li>#'+x.ticket+' '+x.customer+' — '+x.service+' · '+x.starts_at+' ('+x.status+') '+(x.status==='booked'?'<button onclick="cancel('+x.id+')">Cancel</button>':'')+'</li>').join('')}f.onsubmit=async e=>{e.preventDefault();let r=await fetch('/api/appointments',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(Object.fromEntries(new FormData(f)))});if(!r.ok){alert((await r.json()).error);return}f.reset();load()};async function cancel(id){await fetch('/api/appointments/'+id+'/cancel',{method:'PATCH'});load()}load()</script>""")
if __name__=="__main__": init_db(); app.run(debug=os.environ.get("FLASK_DEBUG")=="1")
else:
 with app.app_context(): init_db()
