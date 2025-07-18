import json

class Student:
    def __init__(self, roll_number: int, name: str, age: int, dept: str, year: str, marks):
        self.roll_number = roll_number
        self.name = name
        self.age = age
        self.dept = dept
        self.year = year
        self.marks = marks
        self.total = 0
        self.percentage = 0
        self.gpa = 0

    def calculate_marks(self):
        self.total = sum(self.marks.values())
        self.percentage = self.total / len(self.marks)
        self.gpa = round(self.percentage / 10, 2)

    def to_dict(self):
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

students = {}

# File Handling

def load_student_data_from_json_file():
    students = {}
    try:
        with open("Student.json", "r") as f:
            data = json.load(f)
            for s in data:
                student = Student(
                    roll_number=int(s.get("roll_no", 0)),
                    name=s.get("name", "Unknown"),
                    age=int(s.get("age", 0)),
                    dept=s.get("dept", "Unknown"),
                    year=s.get("year", "Unknown"),
                    marks=s.get("marks", {})
                )
                student.total = s.get("total", 0)
                student.percentage = s.get("percentage", 0)
                student.gpa = s.get("gpa", 0)
                students[student.roll_number] = student
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return students

def write_all_students_to_json(students):
    with open("Student.json", "w") as f:
        json.dump([s.to_dict() for s in students.values()], f, indent=4)

# Utility

def roll_number_exists(roll_number):
    all_students = load_student_data_from_json_file()
    return roll_number in all_students

# Operations

def add_student():
    students = load_student_data_from_json_file()
    n = int(input("Enter the number of students to add: "))
    for _ in range(n):
        roll_number = int(input("Enter roll number: "))
        if roll_number_exists(roll_number):
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
        students[roll_number] = student
        print("Student added successfully.")

    write_all_students_to_json(students)

def remove_student():
    students = load_student_data_from_json_file()
    roll_number = int(input("Enter roll number to remove: "))
    if roll_number in students:
        del students[roll_number]
        write_all_students_to_json(students)
        print("Student removed successfully.")
    else:
        print("Student not found.")

def update_student():
    students = load_student_data_from_json_file()
    roll_number = int(input("Enter roll number to update: "))
    if roll_number in students:
        student = students[roll_number]
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
            print("Invalid choice.")

        students[roll_number] = student
        write_all_students_to_json(students)
        print("Student data updated successfully.")
    else:
        print("Student not found.")

def generate_report_card():
    students = load_student_data_from_json_file()
    roll_number = int(input("Enter roll number: "))
    if roll_number in students:
        print("\n--- Report Card ---")
        print(json.dumps(students[roll_number].to_dict(), indent=4))
    else:
        print("Student not found.")

# Login Handlers

def admin_login():
    print("Admin Options:\n1. Add Student\n2. Remove Student\n3. Update Student")
    choice = int(input("Enter choice: "))
    if choice == 1:
        add_student()
    elif choice == 2:
        remove_student()
    elif choice == 3:
        update_student()
    else:
        print("Invalid choice.")

def student_login():
    choice = input("Do you want to view your report card? (Y/N): ").lower()
    if choice == 'y':
        generate_report_card()
    elif choice == 'n':
        print("Returning to main menu...")
    else:
        print("Invalid choice.")

def main_menu():
    while True:
        print("\n--- Student Record Manager ---")
        print("1. Admin Login\n2. Student Login\n3. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            username = input("Enter admin username: ")
            password = input("Enter admin password: ")
            if username == "admin" and password == "MyAdminPortal@123":
                admin_login()
            else:
                print("Invalid credentials.")

        elif choice == 2:
            username = input("Enter student username: ")
            password = input("Enter student password: ")
            if username == "student" and password == "MyStudentPortal@123":
                student_login()
            else:
                print("Invalid credentials.")

        elif choice == 3:
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main_menu()
