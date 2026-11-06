from app import app,init_db
from datetime import datetime,timedelta
import pytest
@pytest.fixture
def client(tmp_path):
 app.config["TESTING"]=True; app.config["DATABASE"]=str(tmp_path/"t.db"); init_db(); return app.test_client()
def future(): return (datetime.now()+timedelta(days=2)).replace(hour=12,minute=0,second=0,microsecond=0).isoformat()
def test_booking_and_queue(client):
 r=client.post("/api/appointments",json={"customer":"Asha","service":"Consult","starts_at":future()})
 assert r.status_code==201 and r.json["ticket"]==1
 assert client.get("/api/queue?starts_at="+future()).json[0]["position"]==1
def test_reject_past(client):
 assert client.post("/api/appointments",json={"customer":"A","service":"B","starts_at":"2020-01-01T10:00"}).status_code==400
def test_cancel(client):
 r=client.post("/api/appointments",json={"customer":"A","service":"B","starts_at":future()})
 assert client.patch(f"/api/appointments/{r.json['id']}/cancel").status_code==200
