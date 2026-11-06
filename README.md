<div align="center">

# 📅 SlotSync

### Appointment Booking & Walk-in Queue Manager

A simple booking and queue management system for service desks, clinics, salons, and campus offices.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-See%20LICENSE-lightgrey?style=for-the-badge)

</div>

---

## 📌 Overview

**SlotSync** is an appointment scheduling application built with Flask and SQLite. It helps manage bookings, enforce a fixed capacity for each time slot, generate ticket numbers, handle cancellations, and show customers their live queue positions.

## ✨ Features

- 🗓️ **Appointment booking** — book a service for a selected date and time
- 👥 **Slot capacity** — maximum of three active bookings per time slot
- 🎟️ **Ticket numbering** — generate daily ticket numbers
- ❌ **Cancellation** — cancel active appointments
- 📋 **Daily schedule** — view bookings by date
- 🔢 **Queue position** — check active queue order for a slot
- 💾 **Persistent storage** — save bookings in SQLite
- 🔌 **JSON API** — access booking and queue data

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.10+ | Core programming language |
| Flask | Backend web framework |
| SQLite | Data storage |
| HTML, CSS, JavaScript | Frontend |
| pytest | Automated testing |

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or later
- pip

### Installation

```bash
git clone https://github.com/kalashsri18-crypto/SlotSync.git
cd SlotSync

python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Visit **http://127.0.0.1:5000**. The SQLite database is initialized automatically.

### Configuration

Set the `DATABASE` environment variable to choose a different database path. Use `FLASK_DEBUG=1` only during local development.

## 🔗 API Reference

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/slots?date=YYYY-MM-DD` | List bookings for a date |
| POST | `/api/appointments` | Create an appointment |
| PATCH | `/api/appointments/<id>/cancel` | Cancel an active booking |
| GET | `/api/queue?starts_at=YYYY-MM-DDTHH:MM` | Get active queue and positions |

Example booking request:

```json
{
  "customer": "Asha",
  "service": "Consultation",
  "starts_at": "2026-12-10T12:00"
}
```

Use a future date and time when testing the endpoint.

## 🧪 Run Tests

```bash
pytest -q
```

## 📁 Project Structure

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

## 📍 Current Scope

This is currently a single-location demo with a fixed capacity of three active bookings per time slot. User accounts, staff calendars, notifications, payment processing, and multi-location support are not included yet.

## 👨‍💻 Author

**Kalash Srivastava**  
[GitHub](https://github.com/kalashsri18-crypto) · [LinkedIn](https://www.linkedin.com/in/kalash-srivastava-b6592a3b3) · [Email](mailto:kalashsri18@gmail.com)

---

<div align="center">
  Made with ❤️ by Kalash
</div>
