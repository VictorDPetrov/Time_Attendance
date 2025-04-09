CREATE DATABASE bdintex_zkteco;
USE bdintex_zkteco;

CREATE TABLE logs (
userID INT,
employee VARCHAR(200),
workday DATE,
clockIn TIME,
clockOut TIME,
id INT PRIMARY KEY UNIQUE
);

CREATE TABLE employees (
PID INT PRIMARY KEY AUTO_INCREMENT UNIQUE,
ID INT,
employeeName VARCHAR(300),
cardNumber INT
);

DROP TABLE logs;

ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root123';
FLUSH PRIVILEGES;
