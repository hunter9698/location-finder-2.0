import argparse
import sys
import os
import signal
import webbrowser
import threading
import time
from colorama import Fore, Style, init
from pyngrok import ngrok
from server import run_server

# Initialize colorama
init(autoreset=True)

def signal_handler(sig, frame):
    print(f"\n{Fore.RED}[SHUTDOWN]{Fore.WHITE} Stopping server and exiting...")
    ngrok.kill()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def print_banner():
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}
 #        #######  #####     #    ####### ####### ######  
 #       #     # #     #   # #      #    #     # #     # 
 #       #     # #        #   #     #    #     # #     # 
 #       #     # #       #     #    #    #     # ######  
 #       #     # #       #######    #    #     # #   #   
 #       #     # #     # #     #    #    #     # #    #  
 #######  #######  #####  #     #    #     ####### #     # v2.0
          {Fore.WHITE}ETHICAL GEOLOCATION CAPTURE TOOL
          {Fore.YELLOW}Education • Cybersecurity • Demonstration
    """
    print(banner)

def main():
    parser = argparse.ArgumentParser(description="Ethical Location Finder 2.0")
    parser.add_argument("--port", type=int, default=8080, help="Port to run the Flask server on")
    parser.add_argument("--output", type=str, default="logs/capture.json", help="Output JSON file for logs")
    parser.add_argument("--ngrok", action="store_true", help="Automatically start an ngrok tunnel")
    parser.add_argument("--domain", type=str, default="badge-chevy-mongoose.ngrok-free.dev", help="Static ngrok domain")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose error logging")
    
    args = parser.parse_args()
    
    print_banner()
    print(f"{Fore.BLUE}[INFO]{Fore.WHITE} Starting server on port {args.port}...")
    
    public_url = f"http://localhost:{args.port}"
    
    if args.ngrok:
        print(f"{Fore.BLUE}[INFO]{Fore.WHITE} Starting ngrok tunnel...")
        
        connect_kwargs = {}

        if args.domain and args.domain.strip():
            connect_kwargs["domain"] = args.domain

        try:
            tunnel = ngrok.connect(args.port, **connect_kwargs)
        except Exception:
            print(f"{Fore.YELLOW}[WARN]{Fore.WHITE} Domain failed, switching to random URL...")
            tunnel = ngrok.connect(args.port)

        public_url = tunnel.public_url
        print(f"{Fore.GREEN}[LINK]{Fore.WHITE} Public URL: {Fore.YELLOW}{public_url}")
    
    # Permanent static token for consistent tracking
    token = "win-token-77"
    sharable_link = f"{public_url}/?t={token}"
    
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}[LINK] SHARABLE URL: {Fore.WHITE}{sharable_link}")
    print(f"{Fore.BLUE}[INFO]{Fore.WHITE} Sharing this link will track location with token: {Fore.YELLOW}{token}")
    
    print(f"\n{Fore.GREEN}[READY]{Fore.WHITE} Web server is active. Waiting for consent...")
    print(f"{Fore.CYAN}[CTRL+C]{Fore.WHITE} To stop the application")
    
    # Automatically open in Chrome/Default browser
    def open_browser():
        time.sleep(1.5)
        print(f"{Fore.BLUE}[INFO]{Fore.WHITE} Opening link in browser...")
        webbrowser.open(sharable_link)

    threading.Thread(target=open_browser, daemon=True).start()
    
    run_server(args.port, args.output, args.verbose)

if __name__ == "__main__":
    main()
