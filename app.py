from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from functools import wraps
from werkzeug.utils import secure_filename
import os
import openpyxl
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

# Import all needed functions from database
from database import (
    insert_student,
    get_students,
    get_student_by_id,
    update_student,
    delete_student,
    search_students,
    total_students,
    total_departments,
    connect_db,
    save_attendance,
    create_table,
    create_attendance_table,
    get_attendance_by_date,
    get_attendance_by_student,
    insert_marks,
    student_login,
)

app = Flask(__name__)

# Secret Key
app.secret_key = "studentportal123"

# Upload folder configuration
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'xlsx', 'xls'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# -----------------------------
# INITIALIZE DATABASE ON STARTUP
# -----------------------------
print("🔧 Initializing database...")
try:
    create_table()
    create_attendance_table()
    print("✅ Database tables ready!")
except Exception as e:
    print(f"⚠️ Warning: {e}")

# -----------------------------
# Login Required Decorator
# -----------------------------
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
    if "admin" in session:
        return redirect(url_for("dashboard"))
    
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username == "admin" and password == "admin123":
            session["admin"] = username
            flash("Login Successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid Username or Password", "error")

    return render_template("landing.html")


# -----------------------------
# Admin Login
# -----------------------------
@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():

    if "admin" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

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
    try:
        total = total_students()
        departments = total_departments()
    except Exception as e:
        flash(f"Error loading dashboard: {str(e)}", "error")
        total = 0
        departments = 0

    return render_template(
        "index.html",
        total=total,
        departments=departments
    )


# -----------------------------
# Student Dashboard
# -----------------------------
@app.route("/student-dashboard")
def student_dashboard():

    if "student_id" not in session:

        flash("Please login first.", "error")

        return redirect(url_for("student_login_page"))

    return render_template("student_dashboard.html")


# -----------------------------
# Student Profile
# -----------------------------
@app.route("/my-profile")
def my_profile():

    if "student_id" not in session:

        flash("Please login first.", "error")

        return redirect(url_for("student_login_page"))

    student = get_student_by_id(session["student_id"])

    return render_template(
        "student_profile.html",
        student=student
    )

# -----------------------------
# Logout
# -----------------------------
@app.route("/logout")
def logout():

    session.pop("admin", None)
    session.pop("student_id", None)
    session.pop("student_name", None)
    session.clear()   # Recommended

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
    search = request.args.get("search", "").strip()

    try:
        if search:
            students = search_students(search)
        else:
            students = get_students()
    except Exception as e:
        flash(f"Error fetching students: {str(e)}", "error")
        students = []

    return render_template(
        "students.html",
        students=students
    )

# -----------------------------
# Student Profile (Protected)
# -----------------------------
@app.route("/student/<int:id>")
@login_required
def student_profile(id):
    try:
        student = get_student_by_id(id)
        if student is None:
            flash("Student not found!", "error")
            return redirect(url_for("student_list"))
        return render_template(
            "student_profile.html",
            student=student
        )
    except Exception as e:
        flash(f"Error loading student profile: {str(e)}", "error")
        return redirect(url_for("student_list"))

# -----------------------------
# Edit Student Page (Protected)
# -----------------------------
@app.route("/edit-student/<int:id>")
@login_required
def edit_student(id):
    try:
        student = get_student_by_id(id)
        if student is None:
            flash("Student not found!", "error")
            return redirect(url_for("student_list"))
        return render_template(
            "edit_student.html",
            student=student
        )
    except Exception as e:
        flash(f"Error loading student: {str(e)}", "error")
        return redirect(url_for("student_list"))

# -----------------------------
# Update Student (Protected)
# -----------------------------
@app.route("/update-student/<int:id>", methods=["POST"])
@login_required
def update_student_route(id):
    try:
        name = request.form.get("name", "").strip()
        usn = request.form.get("usn", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        department = request.form.get("department", "").strip()

        if not name:
            flash("Name is required!", "error")
            return redirect(url_for("edit_student", id=id))

        update_student(
            id,
            name,
            usn,
            email,
            phone,
            department,
            
        )

        flash("Student updated successfully!", "success")
        return redirect(url_for("student_list"))
    except Exception as e:
        flash(f"Error updating student: {str(e)}", "error")
        return redirect(url_for("edit_student", id=id))

# -----------------------------
# Upload Students
# -----------------------------
@app.route("/upload-students", methods=["GET", "POST"])
@login_required
def upload_students():

    if request.method == "POST":

        try:

            if "excel_file" not in request.files:
                flash("No file selected!", "error")
                return redirect(url_for("upload_students"))

            excel_file = request.files["excel_file"]

            if excel_file.filename == "":
                flash("Please select an Excel file.", "error")
                return redirect(url_for("upload_students"))

            if not allowed_file(excel_file.filename):
                flash("Please upload only .xlsx or .xls files.", "error")
                return redirect(url_for("upload_students"))

            filename = secure_filename(excel_file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            excel_file.save(file_path)

            workbook = openpyxl.load_workbook(file_path)
            sheet = workbook.active

            imported_count = 0

            for row in sheet.iter_rows(min_row=2, values_only=True):

                if row[0] is None:
                    continue

                name = str(row[0]).strip()
                usn = str(row[1]).strip()
                email = str(row[2]).strip()
                phone = str(row[3]).strip()
                department = str(row[4]).strip()

                # Default Password = USN
                password = usn

                # Default Photo
                photo = ""

                insert_student(
                    name,
                    usn,
                    password,
                    email,
                    phone,
                    department,
                    photo
                )

                imported_count += 1

            workbook.close()

            if os.path.exists(file_path):
                os.remove(file_path)

            flash(f"{imported_count} Students Imported Successfully!", "success")

            return redirect(url_for("student_list"))

        except Exception as e:

            flash(f"Error importing students: {str(e)}", "error")

            return redirect(url_for("upload_students"))

    return render_template("upload_students.html")

# -----------------------------
# Delete Student (Protected)
# -----------------------------
@app.route("/delete-student/<int:id>")
@login_required
def delete_student_route(id):
    try:
        delete_student(id)
        flash("Student deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting student: {str(e)}", "error")
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
        try:
            name = request.form.get("name", "").strip()

            if not name:
                flash("Student name is required.", "error")
                return redirect(url_for("add_student"))

            if not name.replace(" ", "").isalpha():
                flash("Student name should contain only letters.", "error")
                return redirect(url_for("add_student"))

            usn = request.form.get("usn", "").strip()
            email = request.form.get("email", "").strip()
            phone = request.form.get("phone", "").strip()
            department = request.form.get("department", "").strip()
            password = usn
            
            photo = request.files.get("photo")
            photo_filename = ""

            if photo and photo.filename != "":
                if allowed_file(photo.filename):
                    photo_filename = secure_filename(photo.filename)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
                    photo_filename = timestamp + photo_filename
                    photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
                else:
                    flash("Invalid file type! Allowed: png, jpg, jpeg, gif", "error")
                    return redirect(url_for("add_student"))

            insert_student(
                name,
                usn,
                email,
                phone,
                department,
                photo_filename,
                password
            )

            flash(f"Student '{name}' added successfully!", "success")
            return redirect(url_for("student_list"))
            
        except Exception as e:
            flash(f"Error adding student: {str(e)}", "error")
            return redirect(url_for("add_student"))

    return render_template("add_student.html")


# -----------------------------
# Attendance Page
# -----------------------------
@app.route("/attendance", methods=["GET", "POST"])
@login_required
def attendance():
    if request.method == "POST":
        try:
            attendance_date = request.form.get("attendance_date", "").strip()
            
            if not attendance_date:
                flash("Please select a date!", "error")
                return redirect(url_for("attendance"))
            
            students = get_students()
            saved_count = 0
            
            for student in students:
                student_id = student[0]
                status = request.form.get(f"attendance_{student_id}")
                
                if status and status in ["Present", "Absent"]:
                    save_attendance(student_id, attendance_date, status)
                    saved_count += 1
            
            if saved_count > 0:
                flash(f"Attendance saved successfully for {saved_count} students!", "success")
            else:
                flash("No attendance records to save!", "warning")
                
        except Exception as e:
            flash(f"Error saving attendance: {str(e)}", "error")
            
        return redirect(url_for("attendance"))

    try:
        students = get_students()
        today_date = datetime.now().strftime("%Y-%m-%d")
        return render_template(
            "attendance.html",
            students=students,
            today_date=today_date
        )
    except Exception as e:
        flash(f"Error loading attendance page: {str(e)}", "error")
        return render_template("attendance.html", students=[], today_date="")

# -----------------------------
# Attendance Report
# -----------------------------
@app.route("/attendance-report", methods=["GET", "POST"])
@login_required
def attendance_report():
    records = []
    attendance_date = ""

    if request.method == "POST":
        try:
            attendance_date = request.form.get("attendance_date", "").strip()
            if attendance_date:
                records = get_attendance_by_date(attendance_date)
            else:
                flash("Please select a date!", "warning")
        except Exception as e:
            flash(f"Error fetching attendance: {str(e)}", "error")

    return render_template(
        "attendance_report.html",
        records=records,
        attendance_date=attendance_date
    )


# -----------------------------
# My Attendance
# -----------------------------
# -----------------------------
# My Attendance
# -----------------------------
@app.route("/my-attendance")
def my_attendance():

    if "student_id" not in session:

        flash("Please login first.", "error")

        return redirect(url_for("student_login_page"))

    records = get_attendance_by_student(session["student_id"])

    return render_template(
        "my_attendance.html",
        records=records
    )


# -----------------------------
# My Marks
# -----------------------------
@app.route("/my-marks")
def my_marks():

    if "student_id" not in session:
        return redirect(url_for("student_login"))

    return "<h2>My Marks Page - Coming Soon</h2>"

# -----------------------------
# Download Attendance PDF
# -----------------------------
@app.route("/download-attendance-pdf/<attendance_date>")
@login_required
def download_attendance_pdf(attendance_date):
    try:
        records = get_attendance_by_date(attendance_date)
        
        if not records:
            flash("No attendance records found for this date!", "warning")
            return redirect(url_for("attendance_report"))

        filename = f"Attendance_Report_{attendance_date}.pdf"
        
        # Create PDF in a temporary location
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        pdf = SimpleDocTemplate(pdf_path)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title = Paragraph(
            f"<b>Student Attendance Report</b><br/>Date: {attendance_date}",
            styles["Heading1"]
        )
        elements.append(title)
        elements.append(Paragraph("<br/>", styles["Normal"]))
        
        # Table data
        data = [["Sl No", "Name", "USN", "Status"]]
        
        for idx, record in enumerate(records, 1):
            data.append([
                str(idx),
                record[0],  # name
                record[1],  # usn
                record[2]   # status
            ])
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.blue),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 12),
            ('FONTSIZE', (0,1), (-1,-1), 10),
        ]))
        
        elements.append(table)
        pdf.build(elements)
        
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        flash(f"Error generating PDF: {str(e)}", "error")
        return redirect(url_for("attendance_report"))

# -----------------------------
# Student Attendance History
# -----------------------------
@app.route("/student-attendance/<int:student_id>")
@login_required
def student_attendance(student_id):
    try:
        student = get_student_by_id(student_id)
        if student is None:
            flash("Student not found!", "error")
            return redirect(url_for("student_list"))
            
        attendance_records = get_attendance_by_student(student_id)
        return render_template(
            "student_attendance.html",
            student=student,
            records=attendance_records
        )
    except Exception as e:
        flash(f"Error loading attendance: {str(e)}", "error")
        return redirect(url_for("student_list"))
    

# -----------------------------
# Marks Management (Fixed - Single Route)
# -----------------------------
@app.route("/marks", methods=["GET", "POST"])
@login_required
def marks():
    students = get_students()

    if request.method == "POST":
        try:
            student_id = request.form.get("student_id")
            subject = request.form.get("subject", "").strip()
            internal1 = int(request.form.get("internal1", 0))
            internal2 = int(request.form.get("internal2", 0))
            semester_exam = int(request.form.get("semester_exam", 0))

            # Validate inputs
            if not student_id or not subject:
                flash("Student and Subject are required!", "error")
                return redirect(url_for("marks"))

            total = internal1 + internal2 + semester_exam

            # Grade Calculation
            if total >= 135:
                grade = "A+"
            elif total >= 120:
                grade = "A"
            elif total >= 105:
                grade = "B"
            elif total >= 90:
                grade = "C"
            else:
                grade = "F"

            insert_marks(
                student_id,
                subject,
                internal1,
                internal2,
                semester_exam,
                total,
                grade
            )

            flash(f"Marks Added Successfully! Total: {total}, Grade: {grade}", "success")
            return redirect(url_for("marks"))
            
        except ValueError as e:
            flash(f"Invalid numeric value: {str(e)}", "error")
        except Exception as e:
            flash(f"Error adding marks: {str(e)}", "error")

        return redirect(url_for("marks"))

    return render_template("add_marks.html",students=students)



# -----------------------------
# Student Login
# -----------------------------
@app.route("/student-login", methods=["GET", "POST"])
def student_login_page():

    if request.method == "POST":

        usn = request.form["usn"]
        password = request.form["password"]

        student = student_login(usn, password)

        if student:

            session["student_id"] = student[0]
            session["student_name"] = student[1]

            flash("Login Successful!", "success")

            return redirect(url_for("student_dashboard"))

        else:

            flash("Invalid USN or Password", "error")

    return render_template("student_login.html")

# -----------------------------
# Run Flask
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)