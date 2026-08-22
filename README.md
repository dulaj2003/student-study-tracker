# SEUSL StudyTrack

#### Video Demo: Coming soon...

#### Description:

SEUSL StudyTrack is a web-based academic planning application created for students of the South Eastern University of Sri Lanka. I developed this application as my final project for CS50x. The main purpose of the project is to give each student one personal place to organize subjects, assignments, deadlines, and academic progress.

University students normally study several subjects during each academic year and semester. They may also receive different types of academic work, including continuous assessments, projects, quizzes, and in-class assignments. It can become difficult to remember every assigned date, due date, priority, and completion status. I selected this problem because it is connected to my own experience as an undergraduate student and because the finished application can be useful to other students.

## Main Features

Each student can create an individual account using their name, registration number, index number, username, faculty, department, and password. The registration form includes all six faculties and 27 departments of SEUSL. JavaScript updates the department list when a student selects a faculty, making it easier to choose the correct department.

After registration or login, the student sees a personalized dashboard. The dashboard shows the total number of assignments and separate totals for pending, in-progress, completed, overdue, and upcoming assignments. Upcoming assignments are assignments due within the next seven days. An assignment is considered overdue when its due date has passed and its status is not completed.

Students can add subjects using a subject code, subject name, academic year, and semester. They can search their subjects and filter them by year and semester. Subjects can also be edited or deleted. When a subject is deleted, its connected assignments are deleted as well.

The assignment section allows a student to select a subject and enter an assignment type, title, description, assigned date, due date, priority, and status. The supported priorities are Low, Medium, and High. The supported statuses are Pending, In Progress, and Completed. Students can search assignments, filter them by status or priority, edit their information, change their status directly, or delete them.

The profile page displays the logged-in student’s account and university information. A student can change their full name and username. They can also change their password after entering their current password correctly. Passwords are never stored as normal readable text.

## Technologies Used

The back end was developed with Python and Flask. SQLite and SQL are used to store and retrieve the application data. The CS50 SQL library provides the database connection. Werkzeug is used to generate and check secure password hashes. HTML and Jinja create the page structure and display database information. CSS provides the visual design and responsive layout. Basic JavaScript controls the mobile navigation menu, dynamic department selection, delete confirmation, password visibility, and automatic removal of notification messages.

I selected Flask and SQLite because they are suitable for a beginner web developer and connect directly with the Python, SQL, HTML, CSS, JavaScript, and Flask topics covered in CS50x. They also allow the application to run inside the CS50 Codespace without requiring a complicated development environment.

## Project Files

`app.py` is the main application file. It creates the Flask application, connects to the database, manages sessions, and contains the routes for registration, login, logout, the dashboard, subjects, assignments, the directory, and profile editing. It also performs input validation, password hashing, database queries, assignment calculations, and user-ownership checks.

`helpers.py` contains the `login_required` decorator. This reusable function redirects visitors to the login page when they try to open a protected page without signing in.

`schema.sql` defines the five database tables and inserts the 6 faculties and 27 departments. It allows a clean copy of the database to be created when required. `studytrack.db` is the SQLite database used by the running application. `requirements.txt` lists Flask and the CS50 library as the required Python packages.

The `templates` directory contains the Jinja and HTML pages. `layout.html` provides the shared header, responsive navigation, notification area, footer, stylesheet, and JavaScript connection. `index.html`, `directory.html`, and `about.html` create the public pages. `register.html` and `login.html` provide account access. `dashboard.html` displays assignment statistics. `subjects.html` and `subject_form.html` manage subjects. `assignments.html` and `assignment_form.html` manage assignments. `profile.html` and `edit_profile.html` display and update the student profile. `error.html` displays customized 404 and 500 error pages.

The `static` directory contains `styles.css`, `script.js`, and the images used by the interface. `styles.css` controls the colours, spacing, forms, tables, cards, navigation, footer, and mobile layout. `script.js` contains the small interactive features that run in the browser.

## Database Design

The database contains `faculties`, `departments`, `users`, `subjects`, and `assignments` tables. Each department belongs to one faculty. Each user selects one faculty and one department. Each subject belongs to one user, and each assignment belongs to both one user and one subject. Foreign keys connect these records.

I used separate faculty and department tables instead of storing their names repeatedly inside every user record. This reduces duplicated data and ensures that students select from the supported university structure. I included `user_id` in the subjects and assignments tables because every account must have its own private academic information.

## Security and Personalization

Flask sessions store the ID of the logged-in user. Protected routes use `login_required`. Subject and assignment queries include the logged-in `user_id`, so one student cannot normally view, edit, or delete another student’s records by changing a URL. Passwords are processed with Werkzeug password hashing instead of being stored directly. Profile changes require the current password before important account information can be updated.

## Development Process and Design Decisions

I developed the project gradually as a beginner. I first planned the database and created the faculty and department records. I then implemented registration, login, logout, and session protection. After account management worked, I added subject management, followed by assignment management and dashboard calculations. I added searching, filters, profile editing, responsive styling, and JavaScript interactions after the main database features were working.

One design decision was to use three simple assignment statuses rather than a more complicated workflow. This keeps the application easy to understand while still showing work that has not started, work currently being completed, and finished work. I also separated academic year and semester because this makes subject organization and filtering clearer for university students.

## Credits and Disclaimer

Faculty and department information was referenced from the official South Eastern University of Sri Lanka website: https://www.seu.ac.lk/.

The SEUSL name and logo belong to the South Eastern University of Sri Lanka. Campus image credit: https://www.seu.ac.lk/fia/pgfia/images/seusl1.jpg. This application is an independent student project created for CS50x and is not an official SEUSL service.

## AI Assistance

ChatGPT by OpenAI was used as a learning and development assistant during this final project. It helped me understand some Flask, SQLite, validation, debugging, interface-design, and documentation concepts. I reviewed and adapted the assistance, tested the application, and made the final project decisions. AI assistance is also cited in relevant source-code comments in accordance with the CS50 final-project instructions.

## Developer

Dulaj Jayasingha
BICT (Hons) Undergraduate
Department of Information and Communication Technology
Faculty of Technology
South Eastern University of Sri Lanka

GitHub: https://github.com/dulaj2003
LinkedIn: https://www.linkedin.com/in/dulaj-jayasingha
