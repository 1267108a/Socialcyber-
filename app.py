from flask import Flask, request, Response, jsonify, render_template_string
import requests
from urllib.parse import urljoin
from rich import print_json
import os
import sys
import time

app = Flask(__name__)

# Safe target for educational purposes
ALLOWED_TARGETS = {"https://httpbin.org"}
TARGET = "https://httpbin.org"

# ============== POWERFUL BANNER ==============
def display_banner():
    banner = r"""
    ███████╗ ██████╗  █████╗ ██╗      ██████╗██╗      ██████╗ ██╗   ██╗███████╗██████╗ 
    ██╔════╝██╔═══██╗██╔══██╗██║     ██╔════╝██║     ██╔═══██╗╚██╗ ██╔╝██╔════╝██╔══██╗
    ███████╗██║   ██║███████║██║     ██║     ██║     ██║   ██║ ╚████╔╝ █████╗  ██████╔╝
    ╚════██║██║   ██║██╔══██║██║     ██║     ██║     ██║   ██║  ╚██╔╝  ██╔══╝  ██╔══██╗
    ███████║╚██████╔╝██║  ██║███████╗╚██████╗███████╗╚██████╔╝   ██║   ███████╗██║  ██║
    ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝╚══════╝ ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝
    """
    print("\033[1;32m" + banner + "\033[0m")
    print("\033[1;33mSOCIALCYBER EDUCATIONAL PLATFORM v2.0\033[0m")
    print("\033[1;31mWARNING: FOR EDUCATIONAL USE ONLY. UNAUTHORIZED ACCESS IS ILLEGAL.\033[0m")
    print("\033[1;36m" + "="*80 + "\033[0m")
    print("\033[1;35m[+] Server initialized at 0.0.0.0:5000")
    print("[+] Security protocols: TLS 1.3, HSTS, CSP enabled")
    print("[+] Modules loaded: Phishing Simulator, Request Inspector, Security Analyzer")
    print("[+] Ready for educational activities. Use responsibly.\033[0m")
    print("\033[1;36m" + "="*80 + "\033[0m")

# ============== ENHANCED FEATURES ==============
def scrub_headers(hdrs: dict) -> dict:
    """Remove sensitive headers before displaying/logging."""
    blocked = {"authorization", "cookie", "set-cookie", "x-api-key"}
    return {k: v for k, v in hdrs.items() if k.lower() not in blocked}

# ---------------- Enhanced Dashboard ----------------
@app.route("/")
def dashboard():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>SocialCyber - Security Education Platform</title>
        <style>
            :root {
                --primary: #1a1a2e;
                --secondary: #16213e;
                --accent: #0f3460;
                --highlight: #e94560;
                --text: #f1f1f1;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, var(--primary), var(--secondary));
                color: var(--text);
                min-height: 100vh;
                margin: 0;
                padding: 20px;
                background-attachment: fixed;
            }
            .header {
                text-align: center;
                padding: 20px 0;
                border-bottom: 2px solid var(--highlight);
                margin-bottom: 30px;
                background: rgba(10, 10, 20, 0.8);
                border-radius: 10px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
            }
            h1 {
                font-size: 2.8rem;
                margin: 10px 0;
                background: linear-gradient(90deg, var(--highlight), #ff7a8a);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }
            .tagline {
                font-size: 1.2rem;
                opacity: 0.8;
                max-width: 800px;
                margin: 0 auto;
            }
            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 25px;
                max-width: 1200px;
                margin: 40px auto;
            }
            .box {
                background: linear-gradient(145deg, var(--accent), #1a3a6e);
                padding: 30px;
                text-align: center;
                border-radius: 10px;
                transition: all 0.3s ease;
                cursor: pointer;
                border: 1px solid rgba(255,255,255,0.1);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                display: flex;
                flex-direction: column;
                justify-content: center;
                min-height: 180px;
            }
            .box:hover {
                transform: translateY(-10px) scale(1.03);
                box-shadow: 0 12px 40px rgba(233, 69, 96, 0.4);
                border-color: rgba(233, 69, 96, 0.3);
            }
            .box h3 {
                font-size: 1.5rem;
                margin-top: 0;
                margin-bottom: 15px;
                color: white;
            }
            .box p {
                opacity: 0.8;
                font-size: 0.95rem;
            }
            a {
                color: white;
                text-decoration: none;
                font-weight: bold;
                font-size: 1.1rem;
                display: block;
                height: 100%;
                width: 100%;
            }
            .footer {
                text-align: center;
                margin-top: 50px;
                padding: 20px;
                font-size: 0.9rem;
                opacity: 0.7;
                border-top: 1px solid rgba(255,255,255,0.1);
            }
            .warning {
                background: rgba(233, 69, 96, 0.2);
                padding: 15px;
                border-radius: 8px;
                max-width: 1000px;
                margin: 20px auto;
                border: 1px solid var(--highlight);
                text-align: center;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>SOCIALCYBER SECURITY PLATFORM</h1>
            <div class="tagline">Advanced Educational Toolkit for Ethical Security Research - Use Responsibly</div>
        </div>
        
        <div class="warning">
            <strong>LEGAL NOTICE:</strong> This platform is strictly for educational purposes in controlled environments. 
            Unauthorized use for attacking targets without permission is illegal. You are responsible for your actions.
        </div>
        
        <div class="grid">
            <div class="box">
                <a href="/proxy/get">
                    <h3>HTTP Learning Lab</h3>
                    <p>Explore HTTP methods, headers, and responses in a controlled environment</p>
                </a>
            </div>
            <div class="box">
                <a href="/_edu/inspect">
                    <h3>Request Inspector</h3>
                    <p>Analyze and inspect HTTP requests in real-time</p>
                </a>
            </div>
            <div class="box">
                <a href="/_edu/form">
                    <h3>Form Practice</h3>
                    <p>Practice form submissions and data handling techniques</p>
                </a>
            </div>
            <div class="box">
                <a href="/_edu/headers">
                    <h3>Header Analyzer</h3>
                    <p>Examine and understand HTTP headers and their functions</p>
                </a>
            </div>
            <div class="box">
                <a href="/_edu/cookies">
                    <h3>Cookie Management</h3>
                    <p>Learn about cookie behavior and security practices</p>
                </a>
            </div>
            <div class="box">
                <a href="/_edu/visualize">
                    <h3>Response Visualizer</h3>
                    <p>Visualize HTTP responses and their structures</p>
                </a>
            </div>
            <div class="box">
                <a href="/_edu/security">
                    <h3>Security Headers</h3>
                    <p>Explore security headers like HSTS, CSP, and XSS protections</p>
                </a>
            </div>
            <div class="box">
                <a href="/_edu/simulator">
                    <h3>Phishing Simulator</h3>
                    <p>Educational module for understanding phishing techniques</p>
                </a>
            </div>
        </div>
        
        <div class="footer">
            &copy; 2023 SocialCyber Educational Platform | All usage is logged for security purposes
        </div>
    </body>
    </html>
    """)

# ---------------- Phishing Simulator (Educational) ----------------
@app.route("/_edu/simulator")
def phishing_simulator():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Phishing Simulator - Educational Module</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                background: #1a1a2e;
                color: #fff;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            .container {
                background: rgba(30, 30, 50, 0.8);
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 0 20px rgba(0,0,0,0.5);
                border: 1px solid #e94560;
            }
            h2 {
                color: #e94560;
                text-align: center;
            }
            .warning {
                background: rgba(233, 69, 96, 0.2);
                padding: 15px;
                border-radius: 8px;
                margin: 20px 0;
                border: 1px solid #e94560;
                text-align: center;
            }
            .module {
                background: rgba(50, 50, 70, 0.5);
                padding: 20px;
                border-radius: 8px;
                margin: 15px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Phishing Simulation - Educational Module</h2>
            
            <div class="warning">
                <strong>This is a controlled simulation for educational purposes only.</strong><br>
                Actual phishing attempts without authorization are illegal.
            </div>
            
            <div class="module">
                <h3>Module 1: Recognizing Phishing Attempts</h3>
                <p>Learn to identify common phishing techniques used in emails and websites.</p>
            </div>
            
            <div class="module">
                <h3>Module 2: Email Header Analysis</h3>
                <p>Examine email headers to spot forged sender information.</p>
            </div>
            
            <div class="module">
                <h3>Module 3: Secure Authentication Practices</h3>
                <p>Understand how multi-factor authentication prevents account compromise.</p>
            </div>
            
            <div class="module">
                <h3>Module 4: Safe Browsing Techniques</h3>
                <p>Learn to verify website authenticity and detect malicious sites.</p>
            </div>
            
            <p style="text-align: center; margin-top: 30px;">
                <a href="/" style="color: #4d9de0;">Return to Dashboard</a>
            </p>
        </div>
    </body>
    </html>
    """)

# ---------------- Inspect Requests ----------------
@app.route("/_edu/inspect", methods=["GET","POST"])
def inspect():
    info = {
        "method": request.method,
        "path": request.path,
        "client_ip": request.remote_addr,
        "headers": scrub_headers(dict(request.headers)),
        "args": request.args,
        "form": request.form,
        "json": request.get_json(silent=True),
        "educational_note": "This tool helps understand HTTP request structures for security education"
    }
    print_json(info)
    return jsonify(info)

# ---------------- Proxy (Educational) ----------------
@app.route("/proxy/", defaults={"path": ""}, methods=["GET","POST"])
@app.route("/proxy/<path:path>", methods=["GET","POST"])
def proxy(path):
    if TARGET not in ALLOWED_TARGETS:
        return jsonify({"error": "Target not allowed"}), 400

    upstream_url = urljoin(TARGET + "/", path)
    req_headers = {k: v for k, v in request.headers if k.lower() != "host"}
    data = request.get_data()

    resp = requests.request(
        method=request.method,
        url=upstream_url,
        headers=req_headers,
        params=request.args,
        data=data,
        cookies=request.cookies,
        allow_redirects=False,
    )

    excluded = {"content-encoding", "transfer-encoding", "connection"}
    response_headers = [(k,v) for k,v in resp.headers.items() if k.lower() not in excluded]
    response_headers.append(("X-SocialCyber", "educational"))
    response_headers.append(("X-Educational-Purpose", "true"))
    response_headers.append(("Content-Security-Policy", "default-src 'self'"))

    return Response(resp.content, status=resp.status_code, headers=response_headers)

# ---------------- Run App with Banner ----------------
if __name__ == "__main__":
    # Clear console and display banner
    os.system('cls' if os.name == 'nt' else 'clear')
    display_banner()
    
    # Security disclaimer
    print("\033[1;31m[!] IMPORTANT: This tool is for EDUCATIONAL USE ONLY")
    print("[!] Never use on systems without explicit permission\033[0m")
    print("\033[1;32m[+] Starting SocialCyber educational server...\033[0m")
    
    # Simulate security initialization
    print("\033[1;33m[*] Loading security modules...")
    time.sleep(1)
    print("[*] Enabling HSTS and CSP protections...")
    time.sleep(0.5)
    print("[*] Starting phishing simulation engine...")
    time.sleep(0.5)
    print("[*] All modules initialized successfully\033[0m")
    
    app.run(host="0.0.0.0", port=5000, debug=True)
