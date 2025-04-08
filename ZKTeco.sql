CREATE DATABASE bdintex_zkteco;
USE bdintex_zkteco;

CREATE TABLE logs (
userID INT PRIMARY KEY UNIQUE,
employee VARCHAR(200),
workday DATE,
clockIn TIME,
clockOut TIME
);