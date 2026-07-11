import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="A24126551002@Sai",
    database="faculty_leave_management"
)

cursor = db.cursor()