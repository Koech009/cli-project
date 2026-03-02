# 🦠 Outbreak CLI

## 📌 Overview

**Outbreak CLI** is a Python-based command-line application for managing infectious disease outbreak data.

The system provides **role-based access control** for:

- 👑 **Admin**
- 🧑‍⚕️ **Health Worker**
- 👥 **Community Member**

It enables secure user registration, outbreak case reporting, region management, and case tracking — all through an interactive CLI.

This project demonstrates:

- Object-Oriented Programming (OOP)
- Service-layer architecture
- Role-Based Access Control (RBAC)
- Input validation
- File-based data persistence
- Unit testing with pytest

---

## 🚀 Features

### 🔐 User Authentication

- User registration and login
- Role assignment (`admin`, `health_worker`, `community`)
- Secure password hashing
- Email and password validation

### 🧑‍⚕️ Case Management

- Report new outbreak cases
- Update case classification:
  - `suspected`
  - `confirmed`
  - `discarded`
- Update patient status:
  - `under_treatment`
  - `recovered`
  - `deceased`
- View case summaries
- Role-based case access

### 🌍 Region Management

- Add new regions
- Remove regions
- View all registered regions

### ✅ Validation & Data Integrity

- Email format validation
- Strong password enforcement
- Age validation
- ENUM-controlled roles and statuses
- Foreign key relationships enforced at application level

### 💾 Data Persistence

The application uses JSON-based storage:

data/
├── users.json
├── cases.json
└── regions.json

This makes the system lightweight and easy to deploy without requiring a database server.

---

## 🏗️ System Architecture

The project follows a clean layered structure:

Models → Represent system entities
Services → Business logic
Utils → Validation & file handling
Data → Persistent JSON storage
Tests → Unit & integration tests

---

## 📁 Project Structure

outbreak_cli/
├── main.py
├── models/
│ ├── case.py
│ ├── user.py
│ ├── region.py
│ └── person.py
├── services/
│ ├── auth_service.py
│ ├── case_service.py
│ └── region_service.py
├── utils/
│ ├── validators.py
│ ├── file_handler.py
│ └── decorators.py
├── data/
│ ├── users.json
│ ├── cases.json
│ └── regions.json
├── tests/
│ ├── test_auth_service.py
│ ├── test_case.py
│ ├── test_case_service.py
│ ├── test_validators.py
│ ├── test_region_service.py
│ ├── test_user_model.py
│ ├── test_region_model.py
│ ├── test_file_handler.py
│ └── test_main_cli.py
├── db_diagram/
│ ├── outbreak_schema.dbml
│ └── outbreak_schema.png
├── requirements.txt
├── pytest.ini
├── README.md
└── .gitignore

---

## 🗄️ Database Design (DBML Schema)

The system is designed around **three core tables**:

### 👤 Users

- `id` (Primary Key)
- `name`
- `email` (Unique)
- `password_hash`
- `role` (ENUM: `community`, `health_worker`, `admin`)
- `created_at`

### 🌍 Regions

- `id` (Primary Key)
- `name` (Unique)
- `location`
- `created_at`

### 🧑‍⚕️ Cases

- `id` (Primary Key)
- `patient_name`
- `age`
- `gender`
- `region_id` (Foreign Key → Regions)
- `reported_by` (Foreign Key → Users)
- `date_reported`
- `classification_status` (ENUM)
- `patient_status` (ENUM)
- `created_at`
- `updated_at`

### 🔗 Relationships

- One User can report many Cases
- One Region can have many Cases
- Each Case belongs to one Region
- Each Case is reported by one User

**ENUMs** are used to ensure controlled and valid values for:

- User roles
- Case classification
- Patient status

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Koech009/outbreak-tracking-cli-system
cd outbreak-tracking-cli-system
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Run the Application
python main.py
🧪 Running Tests

The project uses pytest for testing.

Run all tests:

pytest


🔐 Role-Based Access Overview
Role	Permissions
👑 Admin	Manage users, Manage regions, View all cases, Monitor outbreak statistics
🧑‍⚕️ Health Worker	View cases, Update classification, Update patient status
👥 Community Member	Register & login, Report suspected cases, View personal reports
📊 Example Workflow

Community member registers

Reports a suspected outbreak case

Health worker reviews and updates classification

Admin monitors statistics and regional distribution

🛠️ Technologies Used

Python 3

Pytest

JSON (file-based persistence)

Rich (for CLI tables, optional)

DBML (for schema design)

🔮 Future Improvements

Replace JSON with SQLite or PostgreSQL

Add advanced search and filtering

Export reports to CSV/PDF

Implement dashboards

Convert CLI into REST API

Deploy as a web-based system

👨‍💻 Author

Ian Kipchirchir Koech
Email: iankipchirchir51@gmail.com

📜 License

This project is developed for academic and demonstration purposes.
```
