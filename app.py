from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/students")
def students():
    return render_template("students.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/add-student", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"]
        usn = request.form["usn"]
        email = request.form["email"]
        phone = request.form["phone"]
        department = request.form["department"]

        print("Student Name :", name)
        print("USN :", usn)
        print("Email :", email)
        print("Phone :", phone)
        print("Department :", department)

    return render_template("add_student.html")


if __name__ == "__main__":
    app.run(debug=True)