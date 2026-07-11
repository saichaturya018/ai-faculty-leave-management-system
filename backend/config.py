import mysql.connector


def get_connection():

    conn=mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="faculty_leave"
    )

    return conn