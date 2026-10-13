# DevOps & Library Management Platform

[![Library Platform CI](https://github.com/vedikapangavhane2007/devops/actions/workflows/ci.yml/badge.svg)](https://github.com/vedikapangavhane2007/devops/actions/workflows/ci.yml)
![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.12-blue.svg)
![Framework](https://img.shields.io/badge/framework-Flask%203.1-black.svg)
![Docker](https://img.shields.io/badge/docker-ready-2496ED.svg)
![Database](https://img.shields.io/badge/database-SQLite3-003B57.svg)

A comprehensive DevOps repository containing academic coursework submissions alongside a containerized, full-stack **Library Management Platform** equipped with automated CI/CD pipelines and Docker containerization.

---

## 📁 Repository Structure

```text
devops/
├── .github/
│   └── workflows/
│       └── ci.yml                            # GitHub Actions CI/CD Pipeline
├── .gitignore                                # Git ignore file
├── README.md                                 # Main repository documentation
├── Vedika_Pangavhane_2125UMLF1022_DevOps_Unit1.docx # Unit 1 DevOps Assignment
├── Vedika_Pangavhane_2125UMLF1022_Devops_Unit2.pdf  # Unit 2 DevOps Assignment
└── Library_Management_Platform_Working/      # Library Management Application
    ├── .github/workflows/ci.yml              # Local workflow specification
    ├── .gitignore                            # Component-specific ignore rules
    ├── Dockerfile                            # Docker container build instructions
    ├── docker-compose.yml                    # Multi-container orchestration config
    ├── requirements.txt                      # Python dependencies
    ├── app.py                                # Main Flask web application & DB setup
    ├── RUN.md                                # Quick-start guide
    ├── docs/
    │   └── UNIT1_IMPLEMENTATION.md           # Implementation specification & MVP details
    ├── static/
    │   └── style.css                         # Custom responsive styles
    └── templates/                            # Jinja2 HTML templates
        ├── base.html
        ├── login.html
        ├── dashboard.html
        ├── books.html
        ├── book_form.html
        ├── issue.html
        ├── transactions.html
        ├── reports.html
        └── users.html
```

---

## 📚 Library Management Platform Overview

The **Library Management Platform** is a role-based web application that streamlines book circulation, user management, and inventory tracking.

### Key Features

- **Role-Based Access Control (RBAC)**: Distinct permissions for `admin`, `librarian`, `student`, and `faculty`.
- **Book Catalog & Search**: Real-time filtering, categorization, shelf location tagging, and status tracking (Available / Issued).
- **Issue & Return Tracking**: Automated issuance records, due dates, return timestamps, and fine calculation (₹5/day overdue).
- **Administrative Reports**: High-level metrics for total inventory, active borrowings, registered patrons, collected fines, and category distributions.
- **Health Check Endpoint**: `/health` endpoint returning JSON status for DevOps monitoring and uptime probes.
- **Zero-Setup Database**: Auto-seeds demo accounts and starter books into SQLite on first initialization.

---

## 👥 Demo Credentials

The platform initializes with pre-configured accounts for testing:

| Role | Email | Password | Permissions |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin@library.com` | `admin123` | Full access: User management, reports, inventory, circulation |
| **Librarian** | `librarian@library.com` | `lib123` | Catalog management, book issue/return, transaction records |
| **Student** | `student@library.com` | `student123` | Book search, personal borrowing history, active fines |
| **Faculty** | `faculty@library.com` | `faculty123` | Book search, borrowing transactions |

---

## 🚀 How to Run Locally

### Prerequisites

- **Python 3.10+** (Python 3.12 recommended)
- **Git**

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/vedikapangavhane2007/devops.git
   cd devops/Library_Management_Platform_Working
   ```

2. **Create and activate a virtual environment**:
   - **Windows**:
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\activate
     ```
   - **Linux / macOS**:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the application**:
   ```bash
   python app.py
   ```

5. **Open in browser**:
   Navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🐳 Running with Docker

### Using Docker Compose (Recommended)

From inside the `Library_Management_Platform_Working/` folder:

```bash
docker compose up --build
```
Access the application at [http://localhost:5000](http://localhost:5000).

### Using the Docker CLI

```bash
docker build -t library-platform .
docker run -d -p 5000:5000 --name library-app library-platform
```

---

## 🔄 CI/CD Automation

This repository includes a **GitHub Actions** workflow (`.github/workflows/ci.yml`) that triggers on every `push` and `pull_request` to `main`:

1. Checks out the repository code.
2. Configures a Python 3.12 environment on Ubuntu.
3. Installs dependencies from `requirements.txt`.
4. Runs bytecode compilation checks on `app.py`.
5. Executes automated database initialization verification to guarantee startup reliability.

---

## 🌐 API & Route Reference

| Method | Endpoint | Access Level | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Public | Redirects to `/dashboard` if logged in, otherwise `/login` |
| `GET`, `POST` | `/login` | Public | Authentication endpoint |
| `GET` | `/logout` | Authenticated | Session invalidation |
| `GET` | `/dashboard` | Authenticated | Role-tailored user dashboard |
| `GET` | `/books` | Authenticated | Book catalog search and inventory view |
| `GET`, `POST` | `/books/add` | Admin / Librarian | Add new book to catalog |
| `GET`, `POST` | `/books/<id>/edit` | Admin / Librarian | Edit existing book metadata |
| `POST` | `/books/<id>/delete`| Admin / Librarian | Delete book from catalog |
| `GET`, `POST` | `/issue` | Admin / Librarian | Issue available book to a patron |
| `GET` | `/transactions` | Authenticated | View borrowing history (filtered by role) |
| `POST` | `/return/<id>` | Admin / Librarian | Return borrowed book and calculate fines |
| `GET` | `/users` | Admin | View registered system users |
| `GET` | `/reports` | Admin | System statistics and category analytics |
| `GET` | `/health` | Public | System health endpoint for uptime checks |

---

## 👩‍💻 Author

**Vedika Pangavhane**  
GitHub: [@vedikapangavhane2007](https://github.com/vedikapangavhane2007)