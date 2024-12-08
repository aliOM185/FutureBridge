 create database students;
use students;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO users (email, password) VALUES ('admin@futurebridge.com', '123456');

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    gpa FLOAT NOT NULL,
    stage VARCHAR(50) NOT NULL,
    department VARCHAR(100) NOT NULL,
    mid_degree FLOAT NOT NULL,
    final_degree FLOAT NOT NULL,
    weekly_schedule TEXT NOT NULL,
    subject varchar(255) NOT NULL);

 
    





















