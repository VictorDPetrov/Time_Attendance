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

DROP TABLE logs;

ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root123';
FLUSH PRIVILEGES;
