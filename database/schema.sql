CREATE DATABASE faculty_leave_management;
USE faculty_leave_management;

CREATE TABLE Faculty (
    faculty_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    department VARCHAR(100),
    email VARCHAR(100),
    subject VARCHAR(100),
    workload INT
);

CREATE TABLE LeaveRequests (
    leave_id INT PRIMARY KEY AUTO_INCREMENT,
    faculty_id INT,
    from_date DATE,
    to_date DATE,
    reason TEXT,
    status VARCHAR(20) DEFAULT 'Pending',

    FOREIGN KEY (faculty_id)
    REFERENCES Faculty(faculty_id)
);

CREATE TABLE Timetable (
    timetable_id INT PRIMARY KEY AUTO_INCREMENT,
    faculty_id INT,
    class_name VARCHAR(50),
    subject VARCHAR(100),
    day VARCHAR(20),
    period_no INT,

    FOREIGN KEY (faculty_id)
    REFERENCES Faculty(faculty_id)
);

CREATE TABLE SubstituteFaculty (
    substitute_id INT PRIMARY KEY AUTO_INCREMENT,
    leave_id INT,
    assigned_faculty INT,
    status VARCHAR(20),

    FOREIGN KEY (leave_id)
    REFERENCES LeaveRequests(leave_id),

    FOREIGN KEY (assigned_faculty)
    REFERENCES Faculty(faculty_id)
);