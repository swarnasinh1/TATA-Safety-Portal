from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "tata_safety_portal_2026"


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        employeeid = request.form.get("employeeid")
        password = request.form.get("password")

        conn = sqlite3.connect("database.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM users
            WHERE employeeid=? AND password=?
        """, (employeeid, password))

        user = cursor.fetchone()
        conn.close()

        if user:
            # FIX: actually set the session so protected routes recognize the login
            session["user_id"] = user["employeeid"]
            session["fullname"] = user["fullname"]
            return redirect("/dashboard")

        return render_template(
            "login.html",
            error="Invalid Employee ID or Password"
        )

    return render_template("login.html")

# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        employeeid = request.form["employeeid"]
        department = request.form["department"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO users
                (fullname, employeeid, department, email, password)
                VALUES (?, ?, ?, ?, ?)
            """, (
                fullname,
                employeeid,
                department,
                email,
                password
            ))

            conn.commit()

        except sqlite3.IntegrityError:
            conn.close()
            return render_template(
                "register.html",
                error="Employee ID or Email already exists."
            )

        conn.close()

        return redirect("/login")

    return render_template("register.html")

# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        fullname=session["fullname"]
    )


# ---------------- REPORT ----------------

@app.route("/report", methods=["GET", "POST"])
def report():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        employee_name = request.form["employeeName"]
        employee_id = request.form["employeeId"]
        department = request.form["department"]
        incident_date = request.form["incidentDate"]
        incident_time = request.form["incidentTime"]
        plant = request.form["plant"]
        location = request.form["location"]
        incident_type = request.form["incidentType"]
        severity = request.form["severity"]
        description = request.form["description"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO reports
            (
                employee_name,
                employee_id,
                department,
                incident_date,
                incident_time,
                plant,
                location,
                incident_type,
                severity,
                description
            )
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (
            employee_name,
            employee_id,
            department,
            incident_date,
            incident_time,
            plant,
            location,
            incident_type,
            severity,
            description
        ))

        conn.commit()
        report_id = cursor.lastrowid
        conn.close()

        return redirect(f"/success/{report_id}")

    return render_template("report.html")


# ---------------- REPORTS ----------------

@app.route("/reports")
def reports():

    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM reports
        ORDER BY id DESC
    """)

    reports = cursor.fetchall()

    conn.close()

    return render_template(
        "reports.html",
        reports=reports
    )


# ---------------- STATISTICS ----------------

@app.route("/statistics")
def statistics():

    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM reports")
    total = cursor.fetchone()[0]

    try:
        cursor.execute("SELECT COUNT(*) FROM reports WHERE status='Open'")
        open_cases = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM reports WHERE status='Closed'")
        closed_cases = cursor.fetchone()[0]

    except:
        open_cases = 0
        closed_cases = 0

    cursor.execute("""
        SELECT incident_type,
               COUNT(*) AS count
        FROM reports
        GROUP BY incident_type
    """)
    incident_stats = cursor.fetchall()

    cursor.execute("""
        SELECT plant,
               COUNT(*) AS count
        FROM reports
        GROUP BY plant
    """)
    plant_stats = cursor.fetchall()

    conn.close()

    return render_template(
        "safety_statistics.html",
        total=total,
        open_cases=open_cases,
        closed_cases=closed_cases,
        incident_stats=incident_stats,
        plant_stats=plant_stats
    )


# ---------------- SUCCESS ----------------

@app.route("/success/<int:report_id>")
def success(report_id):

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "success.html",
        report_id=report_id
    )


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()
    return redirect("/")


# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)