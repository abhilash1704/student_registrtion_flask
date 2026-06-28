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

        department TEXT NOT NULL,
                   
        photo TEXT 
                   

    )

    """)

    connection.commit()

    connection.close()

    print("Students Table Created Successfully!")


# ---------------------------------
# Insert Student
# ---------------------------------
def insert_student(name, usn, email, phone, department, photo):

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO students
        (name, usn, email, phone, department, photo)

        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, usn, email, phone, department, photo))

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
# Search Students
# ---------------------------------
def search_students(keyword):

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute("""

        SELECT *

        FROM students

        WHERE
            name LIKE ?
            OR usn LIKE ?

    """, ('%' + keyword + '%', '%' + keyword + '%'))

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



def update_student(student_id, name, usn, email, phone, department):

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
    """, (
        name,
        usn,
        email,
        phone,
        department,
        student_id
    ))

    connection.commit()

    connection.close()

    print("Student Updated Successfully!")


# ---------------------------------
# Delete Student
# ---------------------------------
def delete_student(student_id):

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    connection.commit()

    connection.close()

    print("Student Deleted Successfully!")



# ---------------------------------
# Count Total Students
# ---------------------------------
def total_students():

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute("""

        SELECT COUNT(*)

        FROM students

    """)

    total = cursor.fetchone()[0]

    connection.close()

    return total

# ---------------------------------
# Count Total Departments
# ---------------------------------
def total_departments():

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute("""

        SELECT COUNT(DISTINCT department)

        FROM students

    """)

    total = cursor.fetchone()[0]

    connection.close()

    return total