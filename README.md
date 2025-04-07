# ZKTeco Flask Attendance Viewer

This is a simple Python Flask web application that connects to two ZKTeco biometric terminals (`K40` models) over the local network, retrieves attendance logs from both, and displays them in a clean web interface.

---

## 🔧 Features

- Connects to multiple ZKTeco terminals via UDP.
- Fetches and displays attendance logs (Terminal, Employee ID, Employee name, Tmestamp, Status - *Clocked In / Clocked Out*).
- Displays logs sorted by timestamp.
- Easy to run locally and customizable.
- Flask-based architecture, easily extendable with database, filters, and exports.

---

## 🖥️ Requirements

- Python 3.7+
- ZKTeco terminals connected on the same network
- Terminals should support the ZKProtocol (port 4370)

---

## 📦 Installation

1. Clone the repository:

```bash
git clone https://github.com/VictorDPetrov/ZKTeco-Time_Attendance.git
cd ZKTeco-Time_Attendance
