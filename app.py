from flask import Flask, render_template, request, redirect, url_for, flash
from database import insert_student, get_students
app = Flask(__name__)

# Secret Key
app.secret_key = "studentportal123"

# Temporary list (Remove this after we start reading from SQLite)
students = []


# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# About Page
# -----------------------------
@app.route("/about")
def about():
    return render_template("about.html")


# -----------------------------
# Students Page
# -----------------------------
@app.route("/students")
def student_list():

    students = get_students()

    return render_template(
        "students.html",
        students=students
    )


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

        # Save into SQLite
        insert_student(
            name,
            usn,
            email,
            phone,
            department
        )

        # (Temporary) Save into Python list so the Student List page still works
        students.append({
            "name": name,
            "usn": usn,
            "email": email,
            "phone": phone,
            "department": department
        })

        flash(f"Student '{name}' added successfully!", "success")

        return redirect(url_for("student_list"))

    return render_template("add_student.html")


# -----------------------------
# Run Flask
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)