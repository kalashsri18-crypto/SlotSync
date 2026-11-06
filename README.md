# SlotSync
### Appointment Booking & Walk-in Queue Manager

SlotSync is a simple appointment and queue management application for small service desks, clinics, salons, and campus offices. It assigns ticket numbers, limits each time slot to three active bookings, supports cancellations, and exposes queue positions through a small JSON API.

> **Repository description:** A Flask + SQLite appointment scheduler with slot capacity, ticket numbering, booking cancellation, and live queue positions.

## Features
- Book an appointment with customer, service, and date/time
- Reject past appointments and incomplete booking details
- Enforce a maximum of three active bookings per time slot
- Generate daily ticket numbers
- View bookings by date
- Cancel active appointments
- Check the live position of customers in a slot
- Persist bookings in SQLite

## Tech stack
- Python 3.10+
- Flask
- SQLite
- HTML, CSS and vanilla JavaScript
- pytest

## Project structure
```text
.
├── app.py
├── requirements.txt
├── tests/
│   └── test_app.py
├── .gitignore
├── LICENSE
└── README.md
```

## Getting started

### 1. Clone the repository
```bash
git clone https://github.com/kalashsri18-crypto/Kalash-2.git
cd Kalash-2
```

### 2. Create and activate a virtual environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 3. Install and run
```bash
pip install -r requirements.txt
python app.py
```
Visit **http://127.0.0.1:5000**.

The SQLite database is initialized automatically. Set the `DATABASE` environment variable to use a different database path. Use `FLASK_DEBUG=1` only during local development.

## API reference

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/slots?date=YYYY-MM-DD` | List bookings for a date |
| POST | `/api/appointments` | Create a booking |
| PATCH | `/api/appointments/<id>/cancel` | Cancel an active booking |
| GET | `/api/queue?starts_at=YYYY-MM-DDTHH:MM` | Get active queue and positions |

Example booking payload:
```json
{
  "customer": "Asha",
  "service": "Consultation",
  "starts_at": "2026-12-10T12:00"
}
```
Use a future date/time when testing the endpoint.

## Run tests
```bash
pytest -q
```

## Current scope
This is a single-location demo with a fixed capacity of three active bookings per time slot. It does not yet include user accounts, staff calendars, notifications, payment processing, or multi-location support.

## License
See [LICENSE](LICENSE).
