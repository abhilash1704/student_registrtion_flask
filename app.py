from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

from database import (
    insert_student,
    get_students,
    get_student_by_id,
    update_student,
    delete_student,
    search_students,
    total_students,
    total_departments
)

app = Flask(__name__)

# Secret Key
app.secret_key = "studentportal123"


# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    total = total_students()

    departments = total_departments()

    return render_template(
        "index.html",
        total=total,
        departments=departments
    )


# -----------------------------
# About Page
# -----------------------------
@app.route("/about")
def about():
    return render_template("about.html")


# -----------------------------
# Student List
# -----------------------------
@app.route("/students")
def student_list():

    search = request.args.get("search")

    if search:

         students = search_students(search)

    else:

        students = get_students()

    return render_template(
        "students.html",
        students=students
    )


# -----------------------------
# Student Profile
# -----------------------------
@app.route("/student/<int:id>")
def student_profile(id):

    student = get_student_by_id(id)

    return render_template(
        "student_profile.html",
        student=student
    )

# -----------------------------
# Edit Student Page
# -----------------------------
@app.route("/edit-student/<int:id>")
def edit_student(id):

    student = get_student_by_id(id)

    return render_template(
        "edit_student.html",
        student=student
    )


# -----------------------------
# Update Student
# -----------------------------
@app.route("/update-student/<int:id>", methods=["POST"])
def update_student_route(id):

    name = request.form["name"]
    usn = request.form["usn"]
    email = request.form["email"]
    phone = request.form["phone"]
    department = request.form["department"]

    update_student(
        id,
        name,
        usn,
        email,
        phone,
        department
    )

    flash("Student updated successfully!", "success")

    return redirect(url_for("student_list"))


# -----------------------------
# Delete Student
# -----------------------------
@app.route("/delete-student/<int:id>")
def delete_student_route(id):

    delete_student(id)

    flash("Student deleted successfully!", "success")

    return redirect(url_for("student_list"))


# -----------------------------
# Contact Page
# -----------------------------
@app.route("/contact")
def contact():
    return render_template("contact.html")


# -----------------------------
# Add Student
# -----------------------------
@app.route("/add-student", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":


        name = request.form["name"]

        # Validate Name
        if not name.replace(" ", "").isalpha():
            flash("Student name should contain only letters.", "error")
            return redirect(url_for("add_student"))

        usn = request.form["usn"]
        email = request.form["email"]
        phone = request.form["phone"]
        department = request.form["department"]
        # Get Uploaded Photo
        photo = request.files["photo"]
        
        photo_filename = ""

        if photo.filename != "":

            photo_filename = secure_filename(photo.filename)

            photo.save(
                os.path.join(
                    "static",
                    "uploads",
                    photo_filename
                )
            )

        # Save Student in SQLite
        insert_student(
            name,
            usn,
            email,
            phone,
            department,
            photo_filename
        )

        

        flash(f"Student '{name}' added successfully!", "success")

        return redirect(url_for("student_list"))

    return render_template("add_student.html")


# ---------------------------------
# Create Faculty Table
# ---------------------------------
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

            designation TEXT NOT NULL

        )

    """)

    connection.commit()

    connection.close()

    print("Faculty Table Created Successfully!")

# -----------------------------
# Run Flask
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
