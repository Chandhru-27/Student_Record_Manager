# 🎓 Student Record Manager

A Python-based command-line application to manage student academic records, including functionalities for admin and student logins, storing data persistently in a JSON file.

## 📁 Files Included

- **`Student_record_manager.py`**: Main Python script implementing the core logic for managing student records.
- **`Student.json`**: Data file storing student records in JSON format.

---

## ⚙️ Features

### ✅ Admin Capabilities:
- **Add Student** – Input name, age, department, year, and subject marks.
- **Remove Student** – Delete records using roll number.
- **Update Student** – Modify age, marks, or academic year.
- **Auto-calculates** total marks, percentage, and GPA on each update.

### 📑 Student Capabilities:
- **View Report Card** – Access detailed report using roll number.

---

## 🔐 Authentication

- **Admin Login**  
  - Username: `admin`  
  - Password: `MyAdminPortal@123`

- **Student Login**  
  - Username: `student`  
  - Password: `MyStudentPortal@123`

---

## 🧠 GPA Calculation Logic

- **Total Marks**: Sum of all subject marks.
- **Percentage**: `Total / Number of Subjects`
- **GPA**: `Percentage / 10`, rounded to two decimal places.

---

## 🚀 How to Run

1. Ensure Python 3.x is installed.
2. Run the script:
   ```bash
   python Student_record_manager.py
