import os
from datetime import date, timedelta
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

# Use an environment secret key, or generate one for development
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or os.urandom(24)

db = SQL("sqlite:///studytrack.db")

#directory, about---------------------------------------------------------------------------------------
@app.route("/")
def index():
    """Landing page."""
    return render_template("index.html")

@app.route("/directory")
def directory():
    """Show faculties and departments."""
    faculties = db.execute("""
        SELECT * FROM faculties
        ORDER BY
            CASE name
                WHEN 'Faculty of Engineering' THEN 1
                WHEN 'Faculty of Technology' THEN 2
                WHEN 'Faculty of Management and Commerce' THEN 3
                WHEN 'Faculty of Applied Sciences' THEN 4
                WHEN 'Faculty of Islamic Studies and Arabic Language' THEN 5
                WHEN 'Faculty of Arts and Culture' THEN 6
                ELSE 7
            END
    """)

    departments = db.execute("""
        SELECT d.*, f.name as faculty_name
        FROM departments d
        JOIN faculties f ON d.faculty_id = f.id
        ORDER BY
            CASE f.name
                WHEN 'Faculty of Engineering' THEN 1
                WHEN 'Faculty of Technology' THEN 2
                WHEN 'Faculty of Management and Commerce' THEN 3
                WHEN 'Faculty of Applied Sciences' THEN 4
                WHEN 'Faculty of Islamic Studies and Arabic Language' THEN 5
                WHEN 'Faculty of Arts and Culture' THEN 6
                ELSE 7
            END,
            d.name
    """)

    return render_template("directory.html", faculties=faculties, departments=departments)

@app.route("/get_departments")
def get_departments():
    """Return departments for a given faculty (JSON)."""
    faculty_id = request.args.get("faculty_id")
    if not faculty_id:
        return []

    departments = db.execute(
        "SELECT id, name FROM departments WHERE faculty_id = ? ORDER BY name",
        faculty_id
    )
    return departments

@app.route("/about")
def about():
    """About the project and developer."""
    return render_template("about.html")

#register-----------------------------------------------------------------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new student."""
    if request.method == "POST":
        full_name = (request.form.get("full_name") or "").strip()
        registration_number = (request.form.get("registration_number") or "").strip()
        index_number = (request.form.get("index_number") or "").strip()
        username = (request.form.get("username") or "").strip()
        faculty_id = (request.form.get("faculty_id") or "").strip()
        department_id = (request.form.get("department_id") or "").strip()
        password = request.form.get("password") or ""
        confirmation = request.form.get("confirmation") or ""

        faculties = db.execute("SELECT * FROM faculties ORDER BY name")

        if not all([full_name, registration_number, index_number, username, faculty_id, department_id, password, confirmation]):
            flash("All fields are required.")
            return render_template("register.html", faculties=faculties)

        if password != confirmation:
            flash("Passwords do not match.")
            return render_template("register.html", faculties=faculties)

        dept_check = db.execute("SELECT id FROM departments WHERE id = ? AND faculty_id = ?",
                                department_id, faculty_id)
        if not dept_check:
            flash("Invalid department selected.")
            return render_template("register.html", faculties=faculties)

        if db.execute("SELECT id FROM users WHERE registration_number = ?", registration_number):
            flash("Registration number already registered.")
            return render_template("register.html", faculties=faculties)

        if db.execute("SELECT id FROM users WHERE index_number = ?", index_number):
            flash("Index number already registered.")
            return render_template("register.html", faculties=faculties)

        if db.execute("SELECT id FROM users WHERE username = ?", username):
            flash("Username already taken.")
            return render_template("register.html", faculties=faculties)

        try:
            hashed = generate_password_hash(password)

            db.execute("""
                INSERT INTO users (full_name, registration_number, index_number, username, faculty_id, department_id, password_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, full_name, registration_number, index_number, username, faculty_id, department_id, hashed)

            new_user = db.execute("SELECT id FROM users WHERE username = ?", username)

            if new_user:
                session["user_id"] = new_user[0]["id"]

                # Calculate User Initials
                name_parts = full_name.split()
                if len(name_parts) > 1:
                    initials = (name_parts[0][0] + name_parts[-1][0]).upper()
                else:
                    initials = name_parts[0][0].upper()
                session["user_initials"] = initials

                flash("Registration successful! Welcome.")
                return redirect("/dashboard")
            else:
                flash("Account created successfully! Please log in.")
                return redirect("/login")

        except Exception as e:
            flash("Something went wrong while creating the account. Please try again.")
            print(f"REGISTRATION ERROR: {e}")
            return render_template("register.html", faculties=faculties)

    else:
        faculties = db.execute("SELECT * FROM faculties ORDER BY name")
        return render_template("register.html", faculties=faculties)

#login--------------------------------------------------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        if not username or not password:
            flash("Username and password required.")
            return render_template("login.html")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 1 or not check_password_hash(rows[0]["password_hash"], password):
            flash("Invalid username or password.")
            return render_template("login.html")

        session["user_id"] = rows[0]["id"]

        # Calculate User Initials
        full_name = rows[0]["full_name"]
        name_parts = full_name.split()
        if len(name_parts) > 1:
            initials = (name_parts[0][0] + name_parts[-1][0]).upper()
        else:
            initials = name_parts[0][0].upper()
        session["user_initials"] = initials

        flash("Logged in successfully.")
        return redirect("/dashboard")

    return render_template("login.html")

#logout-------------------------------------------------------------------------------------------------
@app.route("/logout")
def logout():
    """Log user out."""
    session.clear()
    flash("You have been logged out.")
    return redirect("/")

#dashboard----------------------------------------------------------------------------------------------
@app.route("/dashboard")
@login_required
def dashboard():
    """Student dashboard with stats."""
    user_id = session["user_id"]

    total = db.execute("SELECT COUNT(*) as count FROM assignments WHERE user_id = ?", user_id)[0]["count"]
    pending = db.execute("SELECT COUNT(*) as count FROM assignments WHERE user_id = ? AND status = 'Pending'", user_id)[0]["count"]
    in_progress = db.execute("SELECT COUNT(*) as count FROM assignments WHERE user_id = ? AND status = 'In Progress'", user_id)[0]["count"]
    completed = db.execute("SELECT COUNT(*) as count FROM assignments WHERE user_id = ? AND status = 'Completed'", user_id)[0]["count"]

    today = date.today().isoformat()
    overdue = db.execute("""
        SELECT COUNT(*) as count FROM assignments
        WHERE user_id = ? AND due_date < ? AND status != 'Completed'
    """, user_id, today)[0]["count"]

    next_week = (date.today() + timedelta(days=7)).isoformat()
    upcoming = db.execute("""
        SELECT COUNT(*) as count FROM assignments
        WHERE user_id = ? AND due_date >= ? AND due_date <= ? AND status != 'Completed'
    """, user_id, today, next_week)[0]["count"]

    recent = db.execute("""
        SELECT a.*, s.name as subject_name
        FROM assignments a
        JOIN subjects s ON a.subject_id = s.id
        WHERE a.user_id = ?
        ORDER BY a.due_date ASC
        LIMIT 5
    """, user_id)

    return render_template("dashboard.html",
                           total=total,
                           pending=pending,
                           in_progress=in_progress,
                           completed=completed,
                           overdue=overdue,
                           upcoming=upcoming,
                           recent=recent)

#list---------------------------------------------------------------------------------------------------
@app.route("/subjects")
@login_required
def subjects():
    user_id = session["user_id"]
    search = request.args.get("search")
    year_filter = request.args.get("year")
    semester_filter = request.args.get("semester")

    query = "SELECT * FROM subjects WHERE user_id = ?"
    params = [user_id]

    if search:
        query += " AND (code LIKE ? OR name LIKE ?)"
        params.append(f"%{search}%")
        params.append(f"%{search}%")
    if year_filter:
        query += " AND year = ?"
        params.append(year_filter)
    if semester_filter:
        query += " AND semester = ?"
        params.append(semester_filter)

    query += " ORDER BY year, semester, code ASC"

    subjects = db.execute(query, *params)

    return render_template("subjects.html", subjects=subjects, search=search, year_filter=year_filter, semester_filter=semester_filter)

@app.route("/assignments")
@login_required
def assignments():
    user_id = session["user_id"]
    status_filter = request.args.get("status")
    priority_filter = request.args.get("priority")
    search = request.args.get("search")

    query = """
        SELECT a.*, s.code as subject_code, s.name as subject_name
        FROM assignments a
        JOIN subjects s ON a.subject_id = s.id
        WHERE a.user_id = ?
    """
    params = [user_id]

    if status_filter and status_filter in ["Pending", "In Progress", "Completed"]:
        query += " AND a.status = ?"
        params.append(status_filter)
    if priority_filter and priority_filter in ["Low", "Medium", "High"]:
        query += " AND a.priority = ?"
        params.append(priority_filter)
    if search:
        query += " AND (a.title LIKE ? OR a.description LIKE ?)"
        params.append(f"%{search}%")
        params.append(f"%{search}%")

    query += " ORDER BY a.due_date ASC"
    assignments = db.execute(query, *params)

    subjects = db.execute("SELECT id, code, name FROM subjects WHERE user_id = ?", user_id)

    return render_template("assignments.html",
                           assignments=assignments,
                           subjects=subjects,
                           status_filter=status_filter,
                           priority_filter=priority_filter,
                           search=search)

#add----------------------------------------------------------------------------------------------------
@app.route("/subjects/add", methods=["GET", "POST"])
@login_required
def add_subject():
    user_id = session["user_id"]
    if request.method == "POST":
        code = (request.form.get("code") or "").strip()
        name = (request.form.get("name") or "").strip()
        year = (request.form.get("year") or "").strip()
        semester = (request.form.get("semester") or "").strip()

        if not code or not name or not year or not semester:
            flash("All fields are required.")
            return render_template("subject_form.html")

        try:
            year = int(year)
            semester = int(semester)
        except ValueError:
            flash("Year or Semester must be valid numbers.")
            return render_template("subject_form.html")

        if year not in range(1, 5) or semester not in (1, 2):
            flash("Please select a valid year and semester.")
            return render_template("subject_form.html")

        existing = db.execute("SELECT id FROM subjects WHERE user_id = ? AND code = ?", user_id, code)
        if existing:
            flash("You already have a subject with this code.")
            return render_template("subject_form.html")

        db.execute("""
            INSERT INTO subjects (user_id, code, name, year, semester)
            VALUES (?, ?, ?, ?, ?)
        """, user_id, code, name, year, semester)

        flash("Subject added.")
        return redirect("/subjects")

    else:
        return render_template("subject_form.html")

@app.route("/assignments/add", methods=["GET", "POST"])
@login_required
def add_assignment():
    user_id = session["user_id"]
    if request.method == "POST":
        subject_id = (request.form.get("subject_id") or "").strip()
        title = (request.form.get("title") or "").strip()
        description = (request.form.get("description") or "").strip()
        assigned_date = (request.form.get("assigned_date") or "").strip()
        due_date = (request.form.get("due_date") or "").strip()
        assignment_type = (request.form.get("assignment_type") or "").strip()
        priority = (request.form.get("priority") or "").strip()
        status = (request.form.get("status") or "").strip()

        if not all([subject_id, title, assigned_date, due_date, assignment_type, priority, status]):
            flash("All fields are required.")
            subjects = db.execute("SELECT id, code, name FROM subjects WHERE user_id = ?", user_id)
            return render_template("assignment_form.html", subjects=subjects)

        if assignment_type not in ("CA", "Projects", "Quiz", "Inclass"):
            flash("Invalid assignment type.")
            subjects = db.execute(
                "SELECT id, code, name FROM subjects WHERE user_id = ?",
                user_id
            )
            return render_template("assignment_form.html", subjects=subjects)

        if priority not in ("Low", "Medium", "High"):
            flash("Invalid priority.")
            subjects = db.execute(
                "SELECT id, code, name FROM subjects WHERE user_id = ?",
                user_id
            )
            return render_template("assignment_form.html", subjects=subjects)

        if status not in ("Pending", "In Progress", "Completed"):
            flash("Invalid status.")
            subjects = db.execute(
                "SELECT id, code, name FROM subjects WHERE user_id = ?",
                user_id
            )
            return render_template("assignment_form.html", subjects=subjects)

        try:
            assigned = date.fromisoformat(assigned_date)
            due = date.fromisoformat(due_date)
        except ValueError:
            flash("Please enter valid assignment dates.")
            subjects = db.execute(
                "SELECT id, code, name FROM subjects WHERE user_id = ?",
                user_id
            )
            return render_template("assignment_form.html", subjects=subjects)

        if due < assigned:
            flash("Due date cannot be earlier than the assigned date.")
            subjects = db.execute(
                "SELECT id, code, name FROM subjects WHERE user_id = ?",
                user_id
            )
            return render_template("assignment_form.html", subjects=subjects)

        subject_check = db.execute("SELECT id FROM subjects WHERE id = ? AND user_id = ?", subject_id, user_id)
        if not subject_check:
            flash("Invalid subject selected.")
            subjects = db.execute("SELECT id, code, name FROM subjects WHERE user_id = ?", user_id)
            return render_template("assignment_form.html", subjects=subjects)

        db.execute("""
            INSERT INTO assignments (user_id, subject_id, title, description, assigned_date, due_date, assignment_type, priority, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, user_id, subject_id, title, description, assigned_date, due_date, assignment_type, priority, status)

        flash("Assignment added.")
        return redirect("/assignments")

    else:
        subjects = db.execute("SELECT id, code, name FROM subjects WHERE user_id = ?", user_id)
        return render_template("assignment_form.html", subjects=subjects)

#assignments status update------------------------------------------------------------------------------------------
@app.route("/assignments/status/<int:id>", methods=["POST"])
@login_required
def update_assignment_status(id):
    user_id = session["user_id"]
    status = request.form.get("status")

    if status not in ("Pending", "In Progress", "Completed"):
        flash("Invalid status provided.")
        return redirect("/assignments")

    assignment = db.execute("SELECT id FROM assignments WHERE id = ? AND user_id = ?", id, user_id)
    if not assignment:
        flash("Assignment not found.")
        return redirect("/assignments")

    db.execute("UPDATE assignments SET status = ? WHERE id = ? AND user_id = ?", status, id, user_id)

    flash("Status updated successfully.")
    return redirect("/assignments")

#edit---------------------------------------------------------------------------------------------------
@app.route("/subjects/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_subject(id):
    user_id = session["user_id"]

    subject = db.execute(
        "SELECT * FROM subjects WHERE id = ? AND user_id = ?",
        id,
        user_id
    )

    if not subject:
        flash("Subject not found.")
        return redirect("/subjects")

    subject = subject[0]

    if request.method == "POST":
        code = (request.form.get("code") or "").strip()
        name = (request.form.get("name") or "").strip()
        year = request.form.get("year")
        semester = request.form.get("semester")

        if not code or not name or not year or not semester:
            flash("All fields are required.")
            return render_template(
                "subject_form.html",
                subject=subject
            )

        try:
            year = int(year)
            semester = int(semester)
        except ValueError:
            flash("Year and semester must be valid numbers.")
            return render_template(
                "subject_form.html",
                subject=subject
            )

        if year not in range(1, 5) or semester not in (1, 2):
            flash("Please select a valid year and semester.")
            return render_template(
                "subject_form.html",
                subject=subject
            )

        existing = db.execute(
            """
            SELECT id FROM subjects
            WHERE user_id = ? AND code = ? AND id != ?
            """,
            user_id,
            code,
            id
        )

        if existing:
            flash("You already have a subject with this code.")
            return render_template(
                "subject_form.html",
                subject=subject
            )

        db.execute(
            """
            UPDATE subjects
            SET code = ?, name = ?, year = ?, semester = ?
            WHERE id = ? AND user_id = ?
            """,
            code,
            name,
            year,
            semester,
            id,
            user_id
        )

        flash("Subject updated.")
        return redirect("/subjects")

    return render_template(
        "subject_form.html",
        subject=subject
    )


@app.route("/assignments/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_assignment(id):
    user_id = session["user_id"]

    assignment = db.execute(
        "SELECT * FROM assignments WHERE id = ? AND user_id = ?",
        id,
        user_id
    )

    if not assignment:
        flash("Assignment not found.")
        return redirect("/assignments")

    assignment = assignment[0]

    subjects = db.execute(
        """
        SELECT id, code, name
        FROM subjects
        WHERE user_id = ?
        ORDER BY code
        """,
        user_id
    )

    if request.method == "POST":
        subject_id = request.form.get("subject_id")
        title = (request.form.get("title") or "").strip()
        description = (request.form.get("description") or "").strip()
        assigned_date = request.form.get("assigned_date")
        due_date = request.form.get("due_date")
        assignment_type = request.form.get("assignment_type")
        priority = request.form.get("priority")
        status = request.form.get("status")

        if not all([
            subject_id,
            title,
            assigned_date,
            due_date,
            assignment_type,
            priority,
            status
        ]):
            flash("All required fields must be completed.")
            return render_template(
                "assignment_form.html",
                assignment=assignment,
                subjects=subjects
            )

        if assignment_type not in (
            "CA",
            "Projects",
            "Quiz",
            "Inclass"
        ):
            flash("Invalid assignment type.")
            return render_template(
                "assignment_form.html",
                assignment=assignment,
                subjects=subjects
            )

        if priority not in ("Low", "Medium", "High"):
            flash("Invalid priority.")
            return render_template(
                "assignment_form.html",
                assignment=assignment,
                subjects=subjects
            )

        if status not in (
            "Pending",
            "In Progress",
            "Completed"
        ):
            flash("Invalid status.")
            return render_template(
                "assignment_form.html",
                assignment=assignment,
                subjects=subjects
            )

        try:
            assigned = date.fromisoformat(assigned_date)
            due = date.fromisoformat(due_date)
        except ValueError:
            flash("Please enter valid assignment dates.")
            return render_template(
                "assignment_form.html",
                assignment=assignment,
                subjects=subjects
            )

        if due < assigned:
            flash("Due date cannot be earlier than the assigned date.")
            return render_template(
                "assignment_form.html",
                assignment=assignment,
                subjects=subjects
            )

        subject_check = db.execute(
            """
            SELECT id FROM subjects
            WHERE id = ? AND user_id = ?
            """,
            subject_id,
            user_id
        )

        if not subject_check:
            flash("Invalid subject selected.")
            return render_template(
                "assignment_form.html",
                assignment=assignment,
                subjects=subjects
            )

        db.execute(
            """
            UPDATE assignments
            SET subject_id = ?,
                title = ?,
                description = ?,
                assigned_date = ?,
                due_date = ?,
                assignment_type = ?,
                priority = ?,
                status = ?
            WHERE id = ? AND user_id = ?
            """,
            subject_id,
            title,
            description,
            assigned_date,
            due_date,
            assignment_type,
            priority,
            status,
            id,
            user_id
        )

        flash("Assignment updated.")
        return redirect("/assignments")

    return render_template(
        "assignment_form.html",
        assignment=assignment,
        subjects=subjects
    )

#delete-------------------------------------------------------------------------------------------------
@app.route("/subjects/delete/<int:id>", methods=["POST"])
@login_required
def delete_subject(id):
    user_id = session["user_id"]
    db.execute("DELETE FROM assignments WHERE user_id = ? AND subject_id = ?", user_id, id)
    db.execute("DELETE FROM subjects WHERE id = ? AND user_id = ?", id, user_id)
    flash("Subject and its assignments deleted.")
    return redirect("/subjects")

@app.route("/assignments/delete/<int:id>", methods=["POST"])
@login_required
def delete_assignment(id):
    user_id = session["user_id"]
    db.execute("DELETE FROM assignments WHERE id = ? AND user_id = ?", id, user_id)
    flash("Assignment deleted.")
    return redirect("/assignments")

#profile------------------------------------------------------------------------------------------------
@app.route("/profile")
@login_required
def profile():
    user_id = session["user_id"]
    user = db.execute("""
        SELECT u.*, f.name as faculty_name, d.name as department_name
        FROM users u
        JOIN faculties f ON u.faculty_id = f.id
        JOIN departments d ON u.department_id = d.id
        WHERE u.id = ?
    """, user_id)
    if not user:
        flash("User not found.")
        return redirect("/")
    return render_template("profile.html", user=user[0])

#edit-profile------------------------------------------------------------------------------------------------
@app.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    user_id = session["user_id"]

    user = db.execute("SELECT * FROM users WHERE id = ?", user_id)
    if not user:
        flash("User not found.")
        return redirect("/")
    user = user[0]

    if request.method == "POST":
        full_name = (request.form.get("full_name") or "").strip()
        username = (request.form.get("username") or "").strip()
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_new_password = request.form.get("confirm_new_password")

        # 1. Validate required fields (Removed index_number)
        if not full_name or not username or not current_password:
            flash("Full Name, Username, and Current Password are required.")
            return render_template("edit_profile.html", user=user)

        # 2. Verify current password
        if not check_password_hash(user["password_hash"], current_password):
            flash("Incorrect current password.")
            return render_template("edit_profile.html", user=user)

        # 3. Check if username is already taken by another user
        existing_user = db.execute("SELECT id FROM users WHERE username = ? AND id != ?", username, user_id)
        if existing_user:
            flash("Username is already taken.")
            return render_template("edit_profile.html", user=user)

        # 4. Prepare for database update
        if new_password:
            if new_password != confirm_new_password:
                flash("New passwords do not match.")
                return render_template("edit_profile.html", user=user)
            hashed_password = generate_password_hash(new_password)

            db.execute("""
                UPDATE users SET full_name = ?, username = ?, password_hash = ?
                WHERE id = ?
            """, full_name, username, hashed_password, user_id)
            flash("Profile and password updated successfully.")
        else:
            db.execute("""
                UPDATE users SET full_name = ?, username = ?
                WHERE id = ?
            """, full_name, username, user_id)
            flash("Profile updated successfully.")

        name_parts = full_name.split()
        if len(name_parts) > 1:
            initials = (name_parts[0][0] + name_parts[-1][0]).upper()
        else:
            initials = name_parts[0][0].upper()
        session["user_initials"] = initials

        return redirect("/profile")

    return render_template("edit_profile.html", user=user)


## Temporary Crash Route - DELETE AFTER TESTING! -------------------------------------------------------------
#@app.route("/crash")
#def force_crash():
#    x = 1 / 0
#    return "This will never execute"
#test link for error500 page - https://symmetrical-doodle-g47w9pg9g75j2999p-5000.app.github.dev/crash


# Error Handlers---------------------------------------------------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, error_message='Page Not Found'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error_code=500, error_message='Internal Server Error'), 500
