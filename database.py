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


# ---------------------------------
# Insert Student
# ---------------------------------
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


# ---------------------------------
# Get One Student By ID
# ---------------------------------
def get_student_by_id(student_id):

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    connection.close()

    return student


create_table()

# ---------------------------------
# Update Student
# ---------------------------------
def update_student(id, name, usn, email, phone, department):

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE students
        SET
            name = ?,
            usn = ?,
            email = ?,
            phone = ?,
            department = ?
        WHERE id = ?
    """, (name, usn, email, phone, department, id))

    connection.commit()

    connection.close()

    print("Student Updated Successfully!")