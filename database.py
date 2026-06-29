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

# Create Faculty Table
def create_faculty_table():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS faculty(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            faculty_id TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            department TEXT NOT NULL,
            designation TEXT NOT NULL,
            photo TEXT
        )
    """)
    connection.commit()
    connection.close()
    print("Faculty Table Created Successfully!")

# Create Attendance Table
def create_attendance_table():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            attendance_date TEXT,
            status TEXT,
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    """)
    connection.commit()
    connection.close()
    print("Attendance Table Created Successfully!")

# Insert Student
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

# Insert Faculty
def insert_faculty(name, faculty_id, email, phone, department, designation, photo):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO faculty
        (name, faculty_id, email, phone, department, designation, photo)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, faculty_id, email, phone, department, designation, photo))
    connection.commit()
    connection.close()
    print("Faculty Saved Successfully!")

# Get All Faculty
def get_faculty():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM faculty")
    faculty = cursor.fetchall()
    connection.close()
    return faculty

# Get All Students
def get_students():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    connection.close()
    return students

# Search Students
def search_students(keyword):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT *
        FROM students
        WHERE name LIKE ? OR usn LIKE ?
    """, ('%' + keyword + '%', '%' + keyword + '%'))
    students = cursor.fetchall()
    connection.close()
    return students

# Get One Student By ID
def get_student_by_id(student_id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()
    connection.close()
    return student

# Update Student
def update_student(student_id, name, usn, email, phone, department):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE students
        SET name = ?, usn = ?, email = ?, phone = ?, department = ?
        WHERE id = ?
    """, (name, usn, email, phone, department, student_id))
    connection.commit()
    connection.close()
    print("Student Updated Successfully!")

# Delete Student
def delete_student(student_id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    connection.commit()
    connection.close()
    print("Student Deleted Successfully!")

# Count Total Students
def total_students():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM students")
    total = cursor.fetchone()[0]
    connection.close()
    return total

# Count Total Departments
def total_departments():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(DISTINCT department) FROM students")
    total = cursor.fetchone()[0]
    connection.close()
    return total

# Get Faculty By ID
def get_faculty_by_id(faculty_id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM faculty WHERE id = ?", (faculty_id,))
    faculty = cursor.fetchone()
    connection.close()
    return faculty

# Count Total Faculty
def total_faculty():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM faculty")
    total = cursor.fetchone()[0]
    connection.close()
    return total

# Save Attendance
def save_attendance(student_id, attendance_date, status):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO attendance (student_id, attendance_date, status)
        VALUES (?, ?, ?)
    """, (student_id, attendance_date, status))
    connection.commit()
    connection.close()
    print("Attendance Saved Successfully!")

# Get Attendance by Date
def get_attendance_by_date(attendance_date):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT a.*, s.name, s.usn 
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        WHERE a.attendance_date = ?
    """, (attendance_date,))
    attendance = cursor.fetchall()
    connection.close()
    return attendance

# Get All Attendance Records
def get_all_attendance():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT a.*, s.name, s.usn 
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        ORDER BY a.attendance_date DESC
    """)
    attendance = cursor.fetchall()
    connection.close()
    return attendance



# ---------------------------------
# Get Attendance By Date
# ---------------------------------
def get_attendance_by_date(attendance_date):

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute("""

        SELECT
            students.name,
            students.usn,
            attendance.status

        FROM attendance

        JOIN students

        ON attendance.student_id = students.id

        WHERE attendance.attendance_date = ?

    """, (attendance_date,))

    records = cursor.fetchall()

    connection.close()

    return records


def get_attendance_by_student(student_id):

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM attendance
        WHERE student_id = ?
    """, (student_id,))

    records = cursor.fetchall()

    connection.close()

    return records


# ---------------------------------
# Insert Marks
# ---------------------------------

def insert_marks(student_id, subject, internal1,
                 internal2, semester_exam,
                 total, grade):

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute("""

        INSERT INTO marks(

            student_id,
            subject,
            internal1,
            internal2,
            semester_exam,
            total,
            grade

        )

        VALUES(?,?,?,?,?,?,?)

    """, (

        student_id,
        subject,
        internal1,
        internal2,
        semester_exam,
        total,
        grade

    ))

    connection.commit()

    connection.close()


# Create Tables Automatically
if __name__ == "__main__":
    create_table()
    create_faculty_table()
    create_attendance_table()