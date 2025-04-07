from flask import Flask, render_template
from zk import ZK

app = Flask(__name__)

# List of your terminals
terminals = [
    {"name": "Terminal 1", "ip": "192.168.2.221"},
    {"name": "Terminal 2", "ip": "192.168.2.222"},
]

# Fetch attendance logs along with user details
def fetch_attendance_from_terminal(ip, label):
    zk = ZK(ip, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=True)
    logs = []
    try:
        conn = zk.connect()
        conn.disable_device()

        # Fetch attendance logs
        attendance = conn.get_attendance()

        # Fetch user data (usernames, user IDs, etc.)
        users = conn.get_users()

        # Create a mapping from user_id to username
        user_dict = {user.user_id: user.name for user in users}

        # Create logs with the terminal name, user ID, username, timestamp, and status
        for log in attendance:
            logs.append({
                "terminal": label,
                "user_id": log.user_id,
                "username": user_dict.get(log.user_id, "Unknown"),  # Get the username if available
                "timestamp": log.timestamp,
                "status": log.status,
            })

        conn.enable_device()
        conn.disconnect()
    except Exception as e:
        print(f"Error connecting to {label} ({ip}):", e)
    return logs

@app.route('/')
def index():
    all_logs = []
    for terminal in terminals:
        logs = fetch_attendance_from_terminal(terminal["ip"], terminal["name"])
        all_logs.extend(logs)

    # Sort all logs by timestamp (newest first)
    all_logs.sort(key=lambda x: x['timestamp'], reverse=True)
    return render_template('index.html', logs=all_logs)

if __name__ == '__main__':
    app.run(debug=True)
