from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from functools import wraps

# Initialize Flask app
app = Flask(__name__, template_folder=r"C:\Users\Dell\source\repos\futurebridge\templates")
app.secret_key = 'your_secret_key'  # Replace with your secret key for flash messages

# Admin credentials (This is just an example; consider using a database for real applications)
admin_credentials = {
    "email": "admin@futurebridge.com",
    "password": "admin123"
}

# Database configuration
db_config = {
    "host": "localhost",   # Replace with your MySQL host
    "user": "ahmed",   # Replace with your MySQL username
    "password": "ahmedwm", # Replace with your MySQL password
    "database": "students"  # Replace with your database name
}

# Function to check if user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# Home route (Login)
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if email == admin_credentials["email"] and password == admin_credentials["password"]:
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password.")
    return render_template("login.html")

# Dashboard route (only accessible after login)
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

# Route to display students
@app.route('/students')
@login_required
def students():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return render_template('students_list.html', students=students)

# Route to add a student
@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        # Get form data
        name = request.form.get("name")
        email = request.form.get("email")
        gpa = request.form.get("gpa")
        department = request.form.get("department")
        stage = request.form.get("stage")
        mid_degree = request.form.get("mid_degree")
        final_degree = request.form.get("final_degree")
        weekly_schedule = request.form.get("weekly_schedule")
        subject = request.form.get("subject")

        # Insert the student into the database
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            query = """
                INSERT INTO students (name, email, gpa, department, stage, mid_degree, final_degree, weekly_schedule, subject)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, email, gpa, department, stage, mid_degree, final_degree, weekly_schedule, subject))
            conn.commit()
            flash("Student added successfully!")
        except mysql.connector.Error as err:
            flash(f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

        return redirect(url_for("students"))

    # Render the "Add Student" form for GET requests
    return render_template("add_student.html")

# Route to delete a student
@app.route('/delete_student/<int:student_id>')
@login_required
def delete_student(student_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = "DELETE FROM students WHERE id = %s"
    cursor.execute(query, (student_id,))
    conn.commit()
    conn.close()
    
    flash("Student deleted successfully!")
    return redirect(url_for('students'))

# Route for GPA calculation
@app.route('/gpa', methods=['GET', 'POST'])
@login_required
def calculate_gpa():
    if request.method == 'POST':
        grades = request.form['grades']
        try:
            grades_list = [float(grade.strip()) for grade in grades.split(',')]
            if grades_list:
                gpa = sum(grades_list) / len(grades_list)
                return render_template('gpa.html', gpa=round(gpa, 2))
        except ValueError:
            flash("Invalid grades. Please enter numeric values separated by commas.")
    return render_template('gpa.html', gpa=None)

# Route to show statistics (GPA distribution)
@app.route('/statistics')
@login_required
def statistics():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT gpa FROM students")
    gpas = [row['gpa'] for row in cursor.fetchall()]
    conn.close()

    # Create GPA distribution chart
    import matplotlib.pyplot as plt
    import io
    import base64

    plt.figure(figsize=(8, 6))
    plt.hist(gpas, bins=5, color='blue', edgecolor='black', alpha=0.7)
    plt.title('GPA Distribution')
    plt.xlabel('GPA')
    plt.ylabel('Number of Students')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    chart_data = base64.b64encode(buf.getvalue()).decode('utf8')
    buf.close()

    return render_template('statistics.html', chart_data=chart_data)

# Logout route
@app.route('/logout')
@login_required
def logout():
    session.pop("logged_in", None)
    flash("You have been logged out.")
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True)
