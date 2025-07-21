# 🎓 Student Record Manager v2

A **Python-based command-line application** for managing student academic records with **robust MySQL database integration**, **multi-admin control**, and **bcrypt-powered authentication** for enhanced security.

---

## 🚀 What’s New in Version 2?

| Feature | Version 1 | Version 2 |
|--------|-----------|-----------|
| Data Storage | JSON file | MySQL database via `.env` configuration |
| Admin Panel | Single hardcoded admin | Add/remove multiple admins dynamically |
| Security | Plaintext login | Secure bcrypt-hashed passwords |
| Functionality | Basic student CRUD | Full CRUD with GPA calculation, authentication, and access control |
| Scalability | Local storage | Remote MySQL hosting ready (Clever Cloud) |
| Code Structure | Monolithic | Modular and maintainable (via `app.py`, `add_primary_admin.py`) |

---

## 📁 Project Structure

- **`app.py`** – Main application logic: database connection, admin/student workflows, secure login system.
- **`add_primary_admin.py`** – One-time script to insert the first admin securely.
- **`.env`** – Stores your secure DB credentials (never expose this file).
- **`requirements.txt`** – (Create manually if needed):  



---

## ⚙️ Core Features

### ✅ Admin Functions
- **Add Student** – Full academic data input.
- **Remove Student** – Delete by roll number.
- **Update Student** – Edit age, marks, or year.
- **Add Admin** – Dynamically register new admins with secure credentials.

### 🧑‍🎓 Student Features
- **Sign Up** – Secure registration with unique username/password.
- **Login** – Authenticated access to view report card.
- **View Report Card** – Displays student GPA, percentage, subject-wise marks, etc.

---

## 🔐 Security & Authentication

- Passwords are **securely hashed using `bcrypt`**.
- Admin and Student accounts are **uniquely verified** using username constraints.
- DB credentials are **hidden and loaded via `.env`** to prevent hardcoded secrets.
- Login includes **limited retry attempts** to protect against brute-force attacks.

---

## 🗃️ Database Details

- Uses **MySQL**; schema includes `students` and `admins` tables.
- Connection handled through environment variables in `.env`:
```env
DB_HOST=...
DB_PORT=3306
DB_NAME=...
DB_USER=...
DB_PASSWORD=...

## Author
Chandhru Loganathan
