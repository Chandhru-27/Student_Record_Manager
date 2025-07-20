from dotenv import load_dotenv
import mysql.connector
import bcrypt
import os

# Load .env file
load_dotenv()

# Get env vars
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Connect to DB
try:
    connection = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = connection.cursor()
    if connection:
        print("✅ Connected to database")
except Exception as e:
    print("❌ Database connection error:", e)
    raise

cursor.execute("""
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

# Create table if not exists
create_table_sql = """
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_name VARCHAR(100),
    username VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255)
);
"""
cursor.execute(create_table_sql)
connection.commit()

# # Insert admin
sql = """
INSERT INTO admins (admin_name, username, password_hash)
VALUES (%s, %s, %s)
"""
password = "MyAdminPortal1@123"
hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

values = ("Admin1", "Admin_1", hashed_pw)

cursor.execute(sql, values)
connection.commit()
print("✅ Admin added successfully")

