from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
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
    total_departments,
    insert_faculty,
    get_faculty,
    get_faculty_by_id,
    connect_db,
)

app = Flask(__name__)

# Secret Key
app.secret_key = "studentportal123"


# ---------------------------------
# Login Required Decorator
# ---------------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            flash("Please login first.", "error")
            return redirect(url_for("home"))
        return f(*args, **kwargs)
    return decorated_function


# -----------------------------
# Home Page = Login Page
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    # If already logged in, redirect to dashboard
    if "admin" in session:
        return redirect(url_for("dashboard"))
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            session["admin"] = username
            flash("Login Successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid Username or Password", "error")

    return render_template("login.html")


# -----------------------------
# Dashboard (Protected)
# -----------------------------
@app.route("/dashboard")
@login_required
def dashboard():
    total = total_students()
    departments = total_departments()

    return render_template(
        "index.html",
        total=total,
        departments=departments
    )


# -----------------------------
# Logout
# -----------------------------
@app.route("/logout")
def logout():
    session.pop("admin", None)
    flash("Logged out successfully!", "success")
    return redirect(url_for("home"))


# -----------------------------
# About Page (Protected)
# -----------------------------
@app.route("/about")
@login_required
def about():
    return render_template("about.html")


# -----------------------------
# Student List (Protected)
# -----------------------------
@app.route("/students")
@login_required
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
# Faculty List (Protected)
# -----------------------------
@app.route("/faculty")
@login_required
def faculty_list():
    faculty = get_faculty()

    return render_template(
        "faculty.html",
        faculty=faculty
    )


# -----------------------------
# Add Faculty (Protected)
# -----------------------------
@app.route("/add-faculty", methods=["GET", "POST"])
@login_required
def add_faculty():
    if request.method == "POST":
        name = request.form["name"]
        faculty_id = request.form["faculty_id"]
        email = request.form["email"]
        phone = request.form["phone"]
        department = request.form["department"]
        designation = request.form["designation"]

        photo = request.files["photo"]
        photo_filename = ""

        if photo.filename != "":
            photo_filename = secure_filename(photo.filename)

            # Create uploads directory if it doesn't exist
            uploads_dir = os.path.join("static", "uploads")
            if not os.path.exists(uploads_dir):
                os.makedirs(uploads_dir)

            photo.save(os.path.join(uploads_dir, photo_filename))

        insert_faculty(
            name,
            faculty_id,
            email,
            phone,
            department,
            designation,
            photo_filename
        )

        flash("Faculty added successfully!", "success")
        return redirect(url_for("faculty_list"))

    return render_template("add_faculty.html")


# -----------------------------
# Student Profile (Protected)
# -----------------------------
@app.route("/student/<int:id>")
@login_required
def student_profile(id):
    student = get_student_by_id(id)
    return render_template(
        "student_profile.html",
        student=student
    )


# -----------------------------
# Edit Student Page (Protected)
# -----------------------------
@app.route("/edit-student/<int:id>")
@login_required
def edit_student(id):
    student = get_student_by_id(id)
    return render_template(
        "edit_student.html",
        student=student
    )


# -----------------------------
# Update Student (Protected)
# -----------------------------
@app.route("/update-student/<int:id>", methods=["POST"])
@login_required
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
# Delete Student (Protected)
# -----------------------------
@app.route("/delete-student/<int:id>")
@login_required
def delete_student_route(id):
    delete_student(id)
    flash("Student deleted successfully!", "success")
    return redirect(url_for("student_list"))


# -----------------------------
# Contact Page (Protected)
# -----------------------------
@app.route("/contact")
@login_required
def contact():
    return render_template("contact.html")


# -----------------------------
# Add Student (Protected)
# -----------------------------
@app.route("/add-student", methods=["GET", "POST"])
@login_required
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

            # Create uploads directory if it doesn't exist
            uploads_dir = os.path.join("static", "uploads")
            if not os.path.exists(uploads_dir):
                os.makedirs(uploads_dir)

            photo.save(os.path.join(uploads_dir, photo_filename))

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


# -----------------------------
# Faculty Profile (Protected)
# -----------------------------
@app.route("/faculty/<int:id>")
@login_required
def faculty_profile(id):
    faculty = get_faculty_by_id(id)
    return render_template(
        "faculty_profile.html",
        faculty=faculty
    )


# -----------------------------
# Run Flask
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)