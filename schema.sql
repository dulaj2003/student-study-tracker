PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS faculties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    faculty_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    UNIQUE(faculty_id, name),
    FOREIGN KEY(faculty_id) REFERENCES faculties(id)
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    registration_number TEXT NOT NULL UNIQUE,
    index_number TEXT NOT NULL UNIQUE,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    faculty_id INTEGER NOT NULL,
    department_id INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(faculty_id) REFERENCES faculties(id),
    FOREIGN KEY(department_id) REFERENCES departments(id)
);

CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    year INTEGER NOT NULL CHECK(year BETWEEN 1 AND 4),
    semester INTEGER NOT NULL CHECK(semester BETWEEN 1 AND 2),
    UNIQUE(user_id, code),
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    assignment_type TEXT NOT NULL DEFAULT 'CA'
        CHECK(assignment_type IN ('CA', 'Projects', 'Quiz', 'Inclass')),
    assigned_date TEXT NOT NULL,
    due_date TEXT NOT NULL,
    priority TEXT NOT NULL DEFAULT 'Medium'
        CHECK(priority IN ('Low', 'Medium', 'High')),
    status TEXT NOT NULL DEFAULT 'Pending'
        CHECK(status IN ('Pending', 'In Progress', 'Completed')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);


-- Faculty of Applied Sciences

INSERT OR IGNORE INTO faculties (name)
VALUES ('Faculty of Applied Sciences');

INSERT OR IGNORE INTO departments (faculty_id, name)
VALUES (
    (SELECT id FROM faculties
     WHERE name = 'Faculty of Applied Sciences'),
    'Department of Biological Sciences'
);

INSERT OR IGNORE INTO departments (faculty_id, name)
VALUES (
    (SELECT id FROM faculties
     WHERE name = 'Faculty of Applied Sciences'),
    'Department of Chemical Sciences'
);

INSERT OR IGNORE INTO departments (faculty_id, name)
VALUES (
    (SELECT id FROM faculties
     WHERE name = 'Faculty of Applied Sciences'),
    'Department of Computer Science'
);

INSERT OR IGNORE INTO departments (faculty_id, name)
VALUES (
    (SELECT id FROM faculties
     WHERE name = 'Faculty of Applied Sciences'),
    'Department of Mathematical Sciences'
);

INSERT OR IGNORE INTO departments (faculty_id, name)
VALUES (
    (SELECT id FROM faculties
     WHERE name = 'Faculty of Applied Sciences'),
    'Department of Physical Sciences'
);


-- Faculty of Arts and Culture

INSERT OR IGNORE INTO faculties (name)
VALUES ('Faculty of Arts and Culture');

INSERT OR IGNORE INTO departments (faculty_id, name)
VALUES (
    (SELECT id FROM faculties
     WHERE name = 'Faculty of Arts and Culture'),
    'Department of Social Sciences'
);

INSERT OR IGNORE INTO departments (faculty_id, name)
VALUES (
    (SELECT id FROM faculties
     WHERE name = 'Faculty of Arts and Culture'),
    'Department of Languages'
);

INSERT OR IGNORE INTO departments (faculty_id, name)
VALUES (
    (SELECT id FROM faculties
     WHERE name = 'Faculty of Arts and Culture'),
    'Department of Geography'
);

INSERT OR IGNORE INTO departments (faculty_id, name)
VALUES (
    (SELECT id FROM faculties
     WHERE name = 'Faculty of Arts and Culture'),
    'Department of Political Science'
);

INSERT OR IGNORE INTO departments (faculty_id, name)
VALUES (
    (SELECT id FROM faculties
     WHERE name = 'Faculty of Arts and Culture'),
    'Department of Economics and Statistics'
);

INSERT OR IGNORE INTO departments (faculty_id, name)
VALUES (
    (SELECT id FROM faculties
     WHERE name = 'Faculty of Arts and Culture'),
    'Department of Sociology'
);

INSERT OR IGNORE INTO departments (faculty_id, name)
VALUES (
    (SELECT id FROM faculties
     WHERE name = 'Faculty of Arts and Culture'),
    'Department of English Language Teaching'
);

INSERT OR IGNORE INTO departments (faculty_id, name)
VALUES (
    (SELECT id FROM faculties
     WHERE name = 'Faculty of Arts and Culture'),
    'Department of Information Technology'
);


-- Faculty of Management and Commerce

INSERT OR IGNORE INTO faculties (name)
VALUES ('Faculty of Management and Commerce');

INSERT OR IGNORE INTO departments (faculty_id, name)
VALUES (
    (SELECT id FROM faculties
     WHERE name = 'Faculty of Management and Commerce'),
    'Department of Accountancy and Finance'
);

INSERT OR IGNORE INTO departments (faculty_id, name)
VALUES (
    (SELECT id FROM faculties
     WHERE name = 'Faculty of Management and Commerce'),
    'Department of Management'
);

INSERT OR IGNORE INTO departments (faculty_id, name)
VALUES (
    (SELECT id FROM faculties
     WHERE name = 'Faculty of Management and Commerce'),
    'Department of Management and Information Technology'
);

INSERT OR IGNORE INTO departments (faculty_id, name)
VALUES (
    (SELECT id FROM faculties
     WHERE name = 'Faculty of Management and Commerce'),
    'Department of Marketing Management'
);


-- Faculty of Islamic Studies and Arabic Language

INSERT OR IGNORE INTO faculties (name)
VALUES ('Faculty of Islamic Studies and Arabic Language');

INSERT OR IGNORE INTO departments (faculty_id, name)
VALUES (
    (SELECT id FROM faculties
     WHERE name = 'Faculty of Islamic Studies and Arabic Language'),
    'Department of Islamic Studies'
);

INSERT OR IGNORE INTO departments (faculty_id, name)
VALUES (
    (SELECT id FROM faculties
     WHERE name = 'Faculty of Islamic Studies and Arabic Language'),
    'Department of Arabic Language'
);

INSERT OR IGNORE INTO departments (faculty_id, name)
VALUES (
    (SELECT id FROM faculties
     WHERE name = 'Faculty of Islamic Studies and Arabic Language'),
    'Interdisciplinary Unit'
);


-- Faculty of Engineering

INSERT OR IGNORE INTO faculties (name)
VALUES ('Faculty of Engineering');

INSERT OR IGNORE INTO departments (faculty_id, name)
VALUES (
    (SELECT id FROM faculties
     WHERE name = 'Faculty of Engineering'),
    'Department of Civil Engineering'
);

INSERT OR IGNORE INTO departments (faculty_id, name)
VALUES (
    (SELECT id FROM faculties
     WHERE name = 'Faculty of Engineering'),
    'Department of Mechanical Engineering'
);

INSERT OR IGNORE INTO departments (faculty_id, name)
VALUES (
    (SELECT id FROM faculties
     WHERE name = 'Faculty of Engineering'),
    'Department of Electrical and Telecommunication Engineering'
);

INSERT OR IGNORE INTO departments (faculty_id, name)
VALUES (
    (SELECT id FROM faculties
     WHERE name = 'Faculty of Engineering'),
    'Department of Computer Science and Engineering'
);

INSERT OR IGNORE INTO departments (faculty_id, name)
VALUES (
    (SELECT id FROM faculties
     WHERE name = 'Faculty of Engineering'),
    'Department of Interdisciplinary Studies'
);


-- Faculty of Technology

INSERT OR IGNORE INTO faculties (name)
VALUES ('Faculty of Technology');

INSERT OR IGNORE INTO departments (faculty_id, name)
VALUES (
    (SELECT id FROM faculties
     WHERE name = 'Faculty of Technology'),
    'Department of Biosystems Technology'
);

INSERT OR IGNORE INTO departments (faculty_id, name)
VALUES (
    (SELECT id FROM faculties
     WHERE name = 'Faculty of Technology'),
    'Department of Information and Communication Technology'
);

COMMIT;
