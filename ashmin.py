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
from getpass import getpass
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

# Tool database
TOOLS = {
    "anon": [
        ["Tor Router", "tor-router", "Route all traffic through Tor network"],
        ["Proxychains", "proxychains", "Proxy client for application redirection"],
        ["Ghost Surf", "ghost-surf", "Military-grade anonymous browsing"]
    ],
    "recon": [
        ["DarkRecon", "darkrecon", "Advanced reconnaissance framework"],
        ["SocialMapper", "socialmapper", "Social media intelligence gathering"],
        ["Network Scanner", "netscan", "Discover hosts and vulnerabilities"]
    ],
    "creds": [
        ["CredHarvester", "credharvester", "Credential harvesting module"],
        ["Session Hijacker", "sessionhijack", "Steal active sessions"],
        ["Password Decryptor", "passdecrypt", "Decrypt captured credentials"]
    ],
    "social_attack": [
        ["SocialStorm", "socialstorm", "Mass social media exploitation"],
        ["ProfileHack", "profilehack", "Social media account takeover"],
        ["FakeFollower", "fakefollower", "Create fake follower networks"]
    ],
    "phishing": [
        ["PhishMaster", "phishmaster", "Advanced phishing framework"],
        ["EvilGinx", "evilginx", "Man-in-the-middle phishing"],
        ["CloneSite", "clonesite", "Website cloning for phishing"]
    ],
    "wireless": [
        ["WiFiStorm", "wifistorm", "WiFi cracking suite"],
        ["AirStrike", "airstrike", "Wireless attack automation"],
        ["Bluetooth Hunter", "bluetoothhunt", "Bluetooth device exploitation"]
    ],
    "web": [
        ["WebHammer", "webhammer", "Web vulnerability scanner"],
        ["XSS-Terminator", "xss-terminator", "Advanced XSS exploitation"],
        ["SQL Dominator", "sqldominator", "SQL injection framework"]
    ],
    "postexp": [
        ["PersistenceKit", "persistencekit", "Maintain access to compromised systems"],
        ["DataExfil", "dataexfil", "Data exfiltration toolkit"],
        ["Keylogger Pro", "keyloggerpro", "Advanced keylogging"]
    ],
    "payload": [
        ["VenomCraft", "venomcraft", "Custom payload generator"],
        ["StealthLoader", "stealthloader", "Undetectable payload loader"],
        ["Ransomware Builder", "ransombuilder", "Ransomware creation toolkit"]
    ],
    "exploit": [
        ["ZeroDay Hunter", "zerodayhunt", "Zero-day vulnerability exploitation"],
        ["ExploitDB", "exploitdb", "Exploit database integration"],
        ["AutoExploit", "autoexploit", "Automated vulnerability exploitation"]
    ],
    "ddos": [
        ["Titanic Flood", "titanicflood", "Massive traffic generation"],
        ["Botnet Controller", "botnetctrl", "Botnet command and control"],
        ["SlowDeath", "slowdeath", "Slowloris-based DDoS attacks"]
    ],
    "stego": [
        ["ShadowHide", "shadowhide", "Advanced data hiding"],
        ["ImageGhost", "imageghost", "Steganography in images"],
        ["AudioCrypt", "audiocrypt", "Hide data in audio files"]
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
    print(f"{Fore.YELLOW}│ {Fore.GREEN}IP Address: {Fore.CYAN}{socket.gethostbyname(socket.gethostname())}")
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
    entry = {
        "timestamp": timestamp,
        "service": service,
        "username": username,
        "password": password,
        "ip": socket.gethostbyname(socket.gethostname())
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
        "status": "Active"
    }
    active_sessions.append(session)
    
    # Save to file
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
    print(f"{Fore.YELLOW}│ {Fore.GREEN}2.{Fore.CYAN} Export sessions")
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
    
    tools = TOOLS.get(module, [])
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
            print(f"{Fore.YELLOW}│ {i+1}. {Fore.CYAN}{tool1[0]}{' '*(col_width-len(tool1[0])} │ {' '*(col_width+4)} │")
    
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
            execute_attack(module, tool)
        elif choice == '2':
            configure_attack(tool)
        elif choice == '3':
            show_documentation(tool_name, tool_cmd)
        else:
            print(f"{Fore.RED}Invalid selection!")

def execute_attack(module, tool):
    """Execute a simulated attack"""
    tool_name, tool_cmd, tool_desc = tool
    target = input(f"{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Enter target: ")
    session_id = create_session(target, module, tool_name)
    
    print(f"\n{Fore.YELLOW}[{Fore.CYAN}*{Fore.YELLOW}] Launching {tool_name} against {Fore.RED}{target}{Fore.YELLOW}...")
    print(f"{Fore.BLUE}┌───{Fore.MAGENTA}[ ATTACK IN PROGRESS ]{Fore.BLUE}───")
    
    # Simulate attack progress
    steps = [
        "Initializing attack vectors",
        "Bypassing security measures",
        "Exploiting vulnerabilities",
        "Establishing persistence",
        "Exfiltrating sensitive data"
    ]
    
    for i, step in enumerate(steps):
        time.sleep(1.2)
        progress = (i+1) * 20
        print(f"{Fore.BLUE}│ {Fore.YELLOW}[{progress}%] {step}...")
        
        # Randomly capture credentials during attacks
        if random.random() > 0.7 and "Cred" not in tool_name:
            services = ["SSH", "FTP", "Web Login", "Database", "Email"]
            service = random.choice(services)
            username = f"user{random.randint(1, 1000)}"
            password = f"Passw0rd{random.randint(100, 999)}!"
            capture_credentials(service, username, password)
            print(f"{Fore.BLUE}│ {Fore.RED}[!] Captured credentials: {service}: {username}/{password}")
    
    # Simulate success or failure
    success = random.random() > 0.2
    if success:
        print(f"{Fore.BLUE}│ {Fore.GREEN}[+] Attack successful! System compromised")
        
        # Capture admin credentials on success
        if random.random() > 0.5:
            capture_credentials("Admin Access", "admin", "P@ssw0rd123!")
            print(f"{Fore.BLUE}│ {Fore.RED}[!] Admin credentials captured: admin/P@ssw0rd123!")
    else:
        print(f"{Fore.BLUE}│ {Fore.RED}[-] Attack failed! Target defenses were stronger than expected")
    
    print(f"{Fore.BLUE}└───{Fore.GREEN} Attack completed! {Fore.BLUE}───{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Press Enter to continue...")

def configure_attack(tool):
    """Configure attack parameters"""
    tool_name, tool_cmd, tool_desc = tool
    
    print(f"\n{Fore.YELLOW}[{Fore.CYAN}*{Fore.YELLOW}] Configuring {tool_name}...")
    print(f"{Fore.BLUE}┌───{Fore.MAGENTA}[ CONFIGURATION OPTIONS ]{Fore.BLUE}───")
    
    # Simulated configuration options
    config_options = {
        "intensity": ["Low", "Medium", "High", "Extreme"],
        "stealth": ["None", "Basic", "Advanced", "Ghost"],
        "payload": ["Standard", "Custom", "Encrypted", "Polymorphic"]
    }
    
    for option, values in config_options.items():
        print(f"{Fore.BLUE}│ {Fore.GREEN}{option.capitalize()}:")
        for i, value in enumerate(values):
            print(f"{Fore.BLUE}│   {i+1}. {value}")
        choice = input(f"{Fore.BLUE}│ {Fore.YELLOW}Select {option} (1-{len(values)}): ")
        
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(values):
                print(f"{Fore.BLUE}│ {Fore.CYAN}Set {option} to {values[choice_idx]}")
        except ValueError:
            print(f"{Fore.BLUE}│ {Fore.RED}Invalid selection! Using default")
    
    print(f"{Fore.BLUE}└───{Fore.GREEN} Configuration saved! {Fore.BLUE}───{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Press Enter to continue...")

def show_documentation(tool_name, tool_cmd):
    """Show simulated documentation"""
    print(f"\n{Fore.YELLOW}[{Fore.CYAN}*{Fore.YELLOW}] {tool_name} Documentation:")
    print(f"{Fore.BLUE}┌───{Fore.MAGENTA}[ TOOL DOCUMENTATION ]{Fore.BLUE}───")
    
    docs = {
        "CredHarvester": [
            "CredHarvester is an advanced credential harvesting tool",
            "Features:",
            "  - Automated credential extraction from memory",
            "  - Browser password decryption",
            "  - Keylogging capabilities",
            "  - Credential database management",
            "Usage:",
            "  credharvester -t <target> -m <method>",
            "Methods:",
            "  - memory: Extract credentials from process memory",
            "  - browser: Decrypt saved browser passwords",
            "  - keylog: Deploy keylogger for credential capture"
        ],
        "SocialStorm": [
            "SocialStorm is a mass social media exploitation tool",
            "Features:",
            "  - Account takeover via session hijacking",
            "  - Mass phishing campaign deployment",
            "  - Fake engagement generation",
            "  - Profile scraping and analysis",
            "Usage:",
            "  socialstorm -p <platform> -t <target>",
            "Supported Platforms:",
            "  - facebook: Facebook account targeting",
            "  - instagram: Instagram exploitation",
            "  - twitter: Twitter account takeover",
            "  - all: Attack all supported platforms"
        ],
        "PhishMaster": [
            "PhishMaster is an advanced phishing framework",
            "Features:",
            "  - Custom phishing page generation",
            "  - Email campaign management",
            "  - Credential capture and storage",
            "  - Two-factor authentication bypass",
            "Usage:",
            "  phishmaster -t <target_service> -c <campaign_name>",
            "Supported Services:",
            "  - google: Google login phishing",
            "  - facebook: Facebook login phishing",
            "  - microsoft: Microsoft account phishing",
            "  - custom: Custom phishing template"
        ],
        "default": [
            f"{tool_name} is a powerful security tool for offensive operations",
            "Key Features:",
            "  - Advanced attack vectors",
            "  - Evasion techniques",
            "  - Automated exploitation",
            "  - Persistent access",
            "  - Data exfiltration",
            "Basic Usage:",
            f"  {tool_cmd} [options] [target]",
            "Common Options:",
            "  -t, --target: Specify target",
            "  -p, --port: Specify port",
            "  -e, --exploit: Specify exploit method",
            "  -s, --stealth: Set stealth level",
            "Advanced Tactics:",
            "  Combine with proxy chains for anonymity",
            "  Use encrypted channels for command and control",
            "  Schedule attacks for maximum impact"
        ]
    }
    
    doc_lines = docs.get(tool_name, docs["default"])
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
        print(f"{Fore.YELLOW}│ {Fore.GREEN}3.{Fore.CYAN} Uninstall framework")
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
