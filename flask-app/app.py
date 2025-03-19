from flask import Flask,  Response
from datetime import datetime
import pytz
import subprocess
import platform  # To detect OS
from collections import OrderedDict
import json 

app = Flask(__name__)

# Function to get IST time
def get_ist_time():
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S')

# Function to get system process list
def get_system_stats():
    try:
        os_type = platform.system()
        
        if os_type == "Linux":
            # Use top command in batch mode (-b) for 1 iteration (-n 1)
            process_output = subprocess.run(["top", "-b", "-n", "1"], capture_output=True, text=True)
        elif os_type == "Windows":
            # Use tasklist on Windows
            process_output = subprocess.run(["tasklist"], capture_output=True, text=True)
        else:
            return ["Error: Unsupported OS"]

        return process_output.stdout.split("\n")[:20]  # Return first 20 lines
    except Exception as e:
        return [f"Error fetching system stats: {str(e)}"]

# API endpoint to fetch system stats
@app.route('/htop', methods=['GET'])
def get_system_info():
    system_info =  OrderedDict({
        "name": "Sneha Gaur",
        "user": "Snehagaur004",
        "Server Time(IST)": get_ist_time(),
        "Top output": get_system_stats()  # Fetch system stats
    })
    return Response(json.dumps(system_info, indent=4), mimetype='application/json')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)