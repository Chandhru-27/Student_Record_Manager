import bcrypt
import mysql
import mysql.connector


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="student_db"
)
cursor = conn.cursor()

password = "MyAdminPortal1@123"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
cursor.execute (
    """ INSERT INTO admins (admin_name , username , password_hash) 
        VALUES ("Admin1" , "Admin_1" , %s)
    """ , (hashed,)
)
conn.commit()


# 3FFM69VaG!6n3tb
# studentportal