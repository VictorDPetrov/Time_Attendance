import io
import csv
import json
from flask import Flask, render_template, Response, jsonify
from zk import ZK
from flask import jsonify, request
from datetime import datetime
import socket
import time

PORT = 4370
TIMEOUT = .5


app = Flask(__name__)

terminals = [
    {"name": "Terminal 1", "ip": "192.168.2.221"},
    {"name": "Terminal 2", "ip": "192.168.2.222"},
]

def check_terminal_status(ip):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((ip, PORT))  # Connect to the device on port 4370
        sock.close()
        
        if result == 0:
            zk = ZK(ip, port=PORT, timeout=TIMEOUT)
            conn = zk.connect()
            if conn:
                conn.disconnect()
                return True
        return False
    except Exception as e:
        print(f"Error checking terminal status for {ip}: {e}")
        return False  # If an error occurs, mark it as offline

def get_connection(ip):
    try:
        zk = ZK(ip, port=PORT, timeout=TIMEOUT, password=0, force_udp=False, ommit_ping=False)
        conn = zk.connect()
        return conn
    except Exception as e:
        print(f"Error connecting to {ip}: {e}")
        return None

@app.route('/api/ping', methods=['POST'])
def api_ping():
    ip = request.json.get('ip')
    conn = get_connection(ip)
    if conn:
        try:
            conn.disconnect()
            return jsonify({"success": True, "message": "Ping successful"})
        except:
            return jsonify({"success": False, "message": "Ping failed"})
    return jsonify({"success": False, "message": "Device offline"})

@app.route('/api/reboot', methods=['POST'])
def reboot_terminal():
    try:
        data = request.get_json()  # Get the JSON data from the request body
        ip = data.get("ip")  # Extract the IP address from the data

        if not ip:
            return jsonify({"success": False, "message": "IP address is required."}), 400

        # Check if the terminal is online (ping it)
        if not check_terminal_status(ip):
            return jsonify({"success": False, "message": "Device is offline, unable to reboot."}), 400

        # Proceed with the reboot process if the device is online
        conn = get_connection(ip)
        if conn:
            try:
                conn.restart()  # Restart the terminal
                return jsonify({"success": True, "message": f"Device at {ip} restarted successfully."})
            except Exception as e:
                print(f"Error restarting device {ip}: {e}")
                return jsonify({"success": False, "message": f"Failed to restart device at {ip}."}), 500
        else:
            return jsonify({"success": False, "message": f"Unable to connect to {ip}."}), 500

    except Exception as e:
        print(f"Error rebooting device {ip}: {e}")
        return jsonify({"success": False, "message": "Failed to restart device."}), 500


@app.route('/api/set_time', methods=['POST'])
def api_set_time():
    ip = request.json.get('ip')
    conn = get_connection(ip)
    if conn:
        try:
            conn.set_time(datetime.now())
            conn.disconnect()
            return jsonify({"success": True, "message": "Time synced successfully"})
        except:
            return jsonify({"success": False, "message": "Set time failed"})
    return jsonify({"success": False, "message": "Device offline"})

@app.route('/api/get_time', methods=['POST'])
def api_get_time():
    ip = request.json.get('ip')
    conn = get_connection(ip)
    if conn:
        try:
            current_time = conn.get_time()
            conn.disconnect()
            return jsonify({"success": True, "time": current_time.strftime('%Y-%m-%d %H:%M:%S')})
        except:
            return jsonify({"success": False, "message": "Failed to get time"})
    return jsonify({"success": False, "message": "Device offline"})

@app.route('/api/refresh', methods=['POST'])
def api_refresh():
    return jsonify({"success": True})  # We’ll reload the page on frontend instead

def fetch_attendance_from_terminal(ip, label):
    zk = ZK(ip, port=PORT, timeout=TIMEOUT, password=0, force_udp=False, ommit_ping=True)
    logs = []
    try:
        conn = zk.connect()
        conn.disable_device()
        attendance = conn.get_attendance()
        users = conn.get_users()
        user_dict = {user.user_id: user.name for user in users}

        for log in attendance:
            status = "Unknown Status"
            log_status = str(log.status).strip()

            if log_status == "1":
                status = "Clocked In"
            elif log_status == "2":
                status = "Clocked Out"
            
            logs.append({
                "terminal": label,
                "user_id": log.user_id,
                "username": user_dict.get(log.user_id, "Unknown"),
                "timestamp": log.timestamp,
                "status": status,
            })

        conn.enable_device()
        conn.disconnect()
    except Exception as e:
        print(f"Error connecting to {label} ({ip}):", e)
        logs.append({
            "terminal": label,
            "user_id": "-",
            "username": "Device Offline",
            "timestamp": "-",
            "status": "Offline"
        })
    return logs


@app.route('/')
def index():
    all_logs = []
    enriched_terminals = []

    for terminal in terminals:
        ip = terminal["ip"]

        status = "On" if check_terminal_status(ip) else "Off"
        user_count = 0
        current_time = "Unavailable"

        try:
            if status == "On":
                conn = get_connection(ip)
                if conn:
                    user_count = len(conn.get_users())
                    current_time = conn.get_time().strftime('%Y-%m-%d %H:%M:%S')
                    conn.disconnect()
        except Exception as e:
            print(f"Error with {terminal['name']} at {ip}:", e)
            status = "Off"

        enriched_terminals.append({
            "name": terminal["name"],
            "ip": ip,
            "status": status,
            "user_count": user_count,
            "current_time": current_time
        })

        if status == "On":
            logs = fetch_attendance_from_terminal(ip, terminal["name"])
            all_logs.extend(logs)
        else:
            all_logs.append({
                "terminal": terminal["name"],
                "user_id": "-",
                "username": "Device Offline",
                "timestamp": "-",
                "status": "Offline"
            })

    all_logs.sort(key=lambda x: x['timestamp'] if x['timestamp'] != "-" else datetime.min, reverse=True)

    return render_template('index.html', logs=all_logs, terminals=enriched_terminals)



@app.route('/export_csv')
def export_csv():
    all_logs = []
    for terminal in terminals:
        logs = fetch_attendance_from_terminal(terminal["ip"], terminal["name"])
        all_logs.extend(logs)

    fieldnames = ['terminal', 'user_id', 'username', 'timestamp', 'status']

    def generate():
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for log in all_logs:
            log['timestamp'] = log['timestamp'].strftime('%Y-%m-%d %H:%M:%S') if hasattr(log['timestamp'], 'strftime') else log['timestamp']
            writer.writerow(log)

        output.seek(0)
        return output.getvalue()

    return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=attendance_logs.csv"})


@app.route('/export_json')
def export_json():
    all_logs = []
    for terminal in terminals:
        logs = fetch_attendance_from_terminal(terminal["ip"], terminal["name"])
        all_logs.extend(logs)

    # Convert datetime objects to strings
    for log in all_logs:
        if hasattr(log['timestamp'], 'strftime'):
            log['timestamp'] = log['timestamp'].strftime('%Y-%m-%d %H:%M:%S')

    return jsonify(all_logs)


if __name__ == '__main__':
    app.run(debug=True)
