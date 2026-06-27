import sqlite3


# Connect Database
def connect_db():

    connection = sqlite3.connect("students.db")

    return connection


# Create Student Table
def create_table():

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS students(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        usn TEXT NOT NULL,

        email TEXT NOT NULL,

        phone TEXT NOT NULL,

        department TEXT NOT NULL

    )

    """)

    connection.commit()

    connection.close()

    print("Students Table Created Successfully!")


# Insert Student into Database
def insert_student(name, usn, email, phone, department):

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO students
        (name, usn, email, phone, department)

        VALUES (?, ?, ?, ?, ?)
    """, (name, usn, email, phone, department))

    connection.commit()

    connection.close()

    print("Student Saved Successfully!")

# ---------------------------------
# Get All Students
# ---------------------------------
def get_students():

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    connection.close()

    return students


create_table()

#students = get_students()

#print(students)