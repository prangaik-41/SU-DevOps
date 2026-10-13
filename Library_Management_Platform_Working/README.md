# Library Management Platform

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.12-blue.svg)](https://python.org)
![Framework](https://img.shields.io/badge/framework-Flask%203.1-black.svg)
![Docker](https://img.shields.io/badge/docker-ready-2496ED.svg)
![Database](https://img.shields.io/badge/database-SQLite3-003B57.svg)

A containerized Flask web application implementing a full-featured, role-based Library Management Platform with catalog search, book circulation, automatic overdue fine calculations, and system health checks.

---

## 👥 Demo Accounts

| Role | Email | Password | Permissions |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin@library.com` | `admin123` | Full access: User management, reports, inventory, circulation |
| **Librarian** | `librarian@library.com` | `lib123` | Catalog management, book issue/return, transaction records |
| **Student** | `student@library.com` | `student123` | Book search, personal borrowing history, active fines |
| **Faculty** | `faculty@library.com` | `faculty123` | Book search, borrowing transactions |

*Note: The SQLite database (`library.db`) is automatically initialized and seeded on first run.*

---

## 🚀 Quick Start

### Local Setup

```bash
# 1. Create and activate virtual environment
python -m venv .venv

# Windows:
.\.venv\Scripts\activate
# Linux / macOS:
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start server
python app.py
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser.

---

## 🐳 Docker Deployment

### Docker Compose
```bash
docker compose up --build
```

### Docker CLI
```bash
docker build -t library-platform .
docker run -d -p 5000:5000 --name library-app library-platform
```

---

## 📋 Features & Specifications

- **Role-Based Access Control**: Decorator-enforced authorization across admin, librarian, faculty, and student roles.
- **Book Catalog**: Searchable collection by title, author, category, ISBN, and shelf.
- **Issue & Return**: Circulation tracking with fine computation (₹5/day overdue).
- **Reports Dashboard**: Aggregated operational metrics and category breakdown.
- **Health Monitoring**: JSON health endpoint at `/health` for DevOps probes and readiness checks.
