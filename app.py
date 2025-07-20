# --------------------------- Header files --------------------------- #
from dotenv import load_dotenv
import mysql.connector
import bcrypt
import json
import os

# --------------------------- Dotenv Handler --------------------------- #
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# --------------------------- Database Handler --------------------------- #
class Database:
    def __init__(self):
        """
        Initialize and connect to the MySQL database.
        """
        try:
            self.connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            self.cursor = self.connection.cursor()

        except mysql.connector.Error as err:
            print(f"❌ Error: {err}")

    def create_table(self):
        """
        Create the 'students' table if it doesn't already exist.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                roll_number INT PRIMARY KEY,
                name VARCHAR(100),
                age INT,
                dept VARCHAR(100),
                year VARCHAR(10),
                marks TEXT,
                total FLOAT,
                percentage FLOAT,
                gpa FLOAT,
                username VARCHAR(100) UNIQUE,
                password_hash VARCHAR(255)
            )
            """
        )

        """
        Create the 'admins' table if it doesn't already exist.
        """
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS admins (
            id INT PRIMARY KEY AUTO_INCREMENT,
            admin_name VARCHAR(100),
            username VARCHAR(100) UNIQUE,
            password_hash VARCHAR(255)
            )
            """
        )

        self.connection.commit()

    def insert_data_student(self, student):
        """
        Insert a new student record into the table.
        """
        sql = """
            INSERT INTO students (roll_number, name, age, dept, year, marks, total, percentage, gpa)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            student.roll_number,
            student.name,
            student.age,
            student.dept,
            student.year,
            json.dumps(student.marks),
            student.total,
            student.percentage,
            student.gpa
        )
        self.cursor.execute(sql, values)
        self.connection.commit()

    def insert_data_admin(self , admin_name , username , hashed_password):
        sql = """
            INSERT INTO admins (admin_name, username , password_hash)
            VALUES (%s, %s, %s)
            """

        values = (
            admin_name,
            username,
            hashed_password
        )

        self.cursor.execute(sql, values)
        self.connection.commit()

    def fetch_admin_password(self , username):
        self.cursor.execute("SELECT password_hash FROM admins WHERE username = %s", (username,))
        return self.cursor.fetchone()

    def delete_student(self, roll_number):
        """
        Delete a student from the database by roll number.
        """
        self.cursor.execute("DELETE FROM students WHERE roll_number = %s", (roll_number,))
        self.connection.commit()

    def update_student(self, student):
        """
        Update an existing student's information.
        """
        sql = """
            UPDATE students
            SET name=%s, age=%s, dept=%s, year=%s, marks=%s, total=%s, percentage=%s, gpa=%s
            WHERE roll_number=%s
        """
        values = (
            student.name,
            student.age,
            student.dept,
            student.year,
            json.dumps(student.marks),
            student.total,
            student.percentage,
            student.gpa,
            student.roll_number
        )
        self.cursor.execute(sql, values)
        self.connection.commit()

    def student_exists(self, roll_number):
        """
        Check if a student with the given roll number exists.
        """
        self.cursor.execute("SELECT 1 FROM students WHERE roll_number = %s", (roll_number,))
        return self.cursor.fetchone() is not None

    def fetch_student(self, roll_number):
        """
        Fetch student data from the database.
        """
        self.cursor.execute("""
            SELECT roll_number, name, age, dept, year, marks, total, percentage, gpa
            FROM students WHERE roll_number = %s
        """, (roll_number,))
        row = self.cursor.fetchone()
        if row:
            return Student(
                roll_number=row[0],
                name=row[1],
                age=row[2],
                dept=row[3],
                year=row[4],
                marks=json.loads(row[5]),
                total=row[6],
                percentage=row[7],
                gpa=row[8]
            )
        return None

    def close(self):
        """
        Close the database connection.
        """
        self.cursor.close()
        self.connection.close()

# --------------------------- Student Class --------------------------- #
class Student:
    def __init__(self, roll_number: int, name: str, age: int, dept: str, year: str, marks,
        total=0, percentage=0, gpa=0
    ):
        self.roll_number = roll_number
        self.name = name
        self.age = age
        self.dept = dept
        self.year = year
        self.marks = marks
        self.total = total
        self.percentage = percentage
        self.gpa = gpa

    def calculate_marks(self):
        """
        Calculate total, percentage, and GPA based on marks.
        """
        self.total = sum(self.marks.values())
        self.percentage = self.total / len(self.marks)
        self.gpa = round(self.percentage / 10, 2)

    def to_dict(self):
        """
        Convert student data to dictionary format.
        """
        return {
            "roll_no": self.roll_number,
            "name": self.name,
            "age": self.age,
            "dept": self.dept,
            "year": self.year,
            "marks": self.marks,
            "total": self.total,
            "percentage": self.percentage,
            "gpa": self.gpa
        }

# --------------------------- Admin Functions --------------------------- #
def add_student():
    db = Database()
    n = int(input("Enter the number of students to add: "))

    for _ in range(n):
        roll_number = int(input("Enter roll number: "))

        if db.student_exists(roll_number):
            print(f"Roll number {roll_number} already exists. Skipping...")
            continue

        name = input("Enter name: ")
        age = int(input("Enter age: "))
        year = input("Enter academic year (I/II/III/IV): ")
        dept = input("Enter department: ")
        marks = {}
        subject_count = int(input("Enter number of subjects: "))

        for i in range(subject_count):
            sub = input(f"Enter subject {i + 1}: ")
            marks[sub] = int(input("Enter marks: "))

        student = Student(roll_number, name, age, dept, year, marks)

        student.calculate_marks()
        db.insert_data_student(student)
        print("✅ Student added successfully.")

    db.close()

def remove_student():
    db = Database()
    roll_number = int(input("Enter roll number to remove: "))

    if db.student_exists(roll_number):
        db.delete_student(roll_number)
        print("✅ Student removed successfully.")

    else:
        print("❌ Student not found.")

    db.close()

def update_student():
    db = Database()
    roll_number = int(input("Enter roll number to update: "))

    if db.student_exists(roll_number):
        student = db.fetch_student(roll_number)
        print("1. Update Age\n2. Update Marks\n3. Update Academic Year")

        choice = int(input("Enter choice: "))

        if choice == 1:
            student.age = int(input("Enter new age: "))

        elif choice == 2:
            subject_count = int(input("Enter number of subjects: "))
            new_marks = {}

            for i in range(subject_count):
                sub = input(f"Enter subject {i + 1}: ")
                new_marks[sub] = int(input("Enter marks: "))

            student.marks = new_marks
            student.calculate_marks()

        elif choice == 3:
            student.year = input("Enter new academic year: ")

        else:
            print("❌ Invalid choice.")

        db.update_student(student)
        print("✅ Student data updated successfully.")

    else:
        print("❌ Student not found.")

    db.close()

# --------------------------- Student Functions --------------------------- #
def generate_report_card():
    db = Database()
    roll_number = int(input("Enter roll number: "))
    if db.student_exists(roll_number):
        student = db.fetch_student(roll_number)
        print("\n--- 📄 Report Card ---")
        print(json.dumps(student.to_dict(), indent=4))
    else:
        print("❌ Student not found.")
    db.close()

# --------------------------- Menu Handlers --------------------------- #
def admin_menu():
    print("Admin Options:\n1. Add Student\n2. Remove Student\n3. Update Student\n4. Add New Admin")
    choice = int(input("Enter choice: "))

    if choice == 1:
        add_student()

    elif choice == 2:
        remove_student()

    elif choice == 3:
        update_student()

    elif choice == 4:
        add_admin()

    else:
        print("❌ Invalid choice.")

def student_menu():
    choice = input("Do you want to view your report card? (Y/N): ").lower()

    if choice == 'y':
        generate_report_card()

    elif choice == 'n':
        print("Returning to main menu...")

    else:
        print("❌ Invalid choice.")

# --------------------------- Security Handlers --------------------------- #

def student_signup():
    db = Database()
    roll_number = input("Enter your roll number: ")

    if db.student_exists(roll_number):
        username = input("Enter username: ")

        while True:
            password = input("Enter new password: ")
            confirm = input("Confirm password: ")
            if confirm == password:
                break
            else:
                print("❌ Passwords do not match. Please try again.")

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        db.cursor.execute(
            """
            UPDATE students 
            SET username = %s, password_hash = %s 
            WHERE roll_number = %s
            """,
            (username, hashed_pw, roll_number)
        )
        db.connection.commit()
        print("✅ Successfully signed up. ")

    else:
        print("❌ Roll number not found. Please contact admin.")
    
    db.close()

def student_login():
    db = Database()
    username = input("Enter username: ")

    result = db.fetch_admin_password(username)

    if not result:
        print("❌ Username not found.")
        db.close()
        return False

    hashed_password = result[0]
    attempts = 3

    while attempts > 0:
        password = input("Enter your password: ")

        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            print("✅ Login successful.")
            return True
        else:
            attempts -= 1
            print(f"❌ Incorrect password. {attempts} attempt(s) left.")

    if attempts == 0:
        print("❌ Maximum attempts reached. Exiting...")
        return False

    db.close()

def admin_login():
    db = Database()
    username = input("Enter username: ")

    result = db.fetch_admin_password(username)

    if not result:
        print("❌ Username not found.")
        db.close()
        return False

    hashed_password = result[0]
    attempts = 3

    while attempts > 0:
        password = input("Enter your password: ")

        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            print("✅ Login successful.")
            return True
        else:
            attempts -= 1
            print(f"❌ Incorrect password. {attempts} attempt(s) left.")

    if attempts == 0:
        print("❌ Maximum attempts reached. Exiting...")
        return False

    db.close()

def add_admin():
    db = Database()

    name = input("Enter admin name: ")
    username = input("Enter username: ")
    
    while True:

        password = input("Enter new password: ")
        confirm = input("Confirm password: ")
        if confirm == password:
            break
        else:
            print("❌ Passwords do not match. Please try again.")

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    db.insert_data_admin(name , username , hashed_pw) 
    db.connection.commit()

    print("✅ Successfully added fellow admin. ")
    
    db.close()
# --------------------------- Main Menu --------------------------- #
def main_menu():
    while True:
        print("\n--- 🎓 Student Record Manager ---")
        print("1. Admin Login\n2. Student Login\n3. Student Signup\n4. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            
            if admin_login():
                admin_menu()
            else:
                print("❌ Invalid credentials.")

        elif choice == 2:

            if student_login():
                student_menu()
            else:
                print("❌ Invalid credentials.")

        elif choice == 3:
            student_signup()

        elif choice == 4:
            print("👋 Exiting application. Goodbye!")
            break

        else:
            print("❌ Invalid choice.")

# --------------------------- Program Entry --------------------------- #
if __name__ == "__main__":
    db = Database()
    db.create_table()
    db.close()
    main_menu()
