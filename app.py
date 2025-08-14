from flask import Flask, request, Response, jsonify, render_template_string
import requests
from urllib.parse import urljoin
from rich import print_json

app = Flask(__name__)

# Safe target for educational purposes
ALLOWED_TARGETS = {"https://httpbin.org"}
TARGET = "https://httpbin.org"

def scrub_headers(hdrs: dict) -> dict:
    """Remove sensitive headers before displaying/logging."""
    blocked = {"authorization", "cookie", "set-cookie"}
    return {k: v for k, v in hdrs.items() if k.lower() not in blocked}

# ---------------- Dashboard ----------------
@app.route("/")
def dashboard():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>SocialCyber - Educational Lab</title>
        <style>
            body { font-family: Arial; background:#1b1b1b; color:#fff; }
            h1 { text-align:center; margin-top:20px; }
            .grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap:20px; max-width:900px; margin:40px auto; }
            .box { background:#2c2c2c; padding:30px; text-align:center; border-radius:10px; transition: 0.3s; cursor:pointer; }
            .box:hover { background:#444; transform: scale(1.05); }
            a { color:#fff; text-decoration:none; font-weight:bold; font-size:18px; }
        </style>
    </head>
    <body>
        <h1>SocialCyber - Educational Lab</h1>
        <div class="grid">
            <div class="box"><a href="/proxy/get">HTTP Learning Lab</a></div>
            <div class="box"><a href="/_edu/inspect">Request Inspector</a></div>
            <div class="box"><a href="/_edu/form">Form Practice</a></div>
            <div class="box"><a href="/_edu/headers">Header Viewer</a></div>
            <div class="box"><a href="/_edu/cookies">Cookie Viewer</a></div>
            <div class="box"><a href="/_edu/visualize">Response Visualizer</a></div>
            <div class="box"><a href="/_edu/security">HSTS & Security Demo</a></div>
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
    }
    return jsonify(info)

# ---------------- Form Practice ----------------
@app.route("/_edu/form", methods=["GET"])
def demo_form():
    return render_template_string("""
    <h2>Form Practice</h2>
    <form action="/proxy/post" method="post">
      <label>Name: <input name="name"></label><br/>
      <label>Email: <input name="email"></label><br/>
      <button type="submit">Submit</button>
    </form>
    <p>This safely posts data to a sandbox environment to illustrate HTTP forms.</p>
    """)

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
    response_headers.append(("X-SocialCyber", "true"))

    return Response(resp.content, status=resp.status_code, headers=response_headers)

# ---------------- Header Viewer ----------------
@app.route("/_edu/headers")
def header_viewer():
    headers = scrub_headers(dict(request.headers))
    print_json(data=headers)
    return jsonify(headers)

# ---------------- Cookie Viewer ----------------
@app.route("/_edu/cookies")
def cookie_viewer():
    cookies = request.cookies
    return jsonify({k:v for k,v in cookies.items()})

# ---------------- Response Visualizer ----------------
@app.route("/_edu/visualize")
def response_visualizer():
    example_response = {
        "message": "This is a safe JSON response example",
        "status": "educational",
        "items": [1,2,3,4]
    }
    print_json(data=example_response)
    return jsonify(example_response)

# ---------------- HSTS & Security Headers Demo ----------------
@app.route("/_edu/security")
def security_demo():
    headers = {
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block"
    }
    return Response("This page demonstrates security headers", headers=headers)

# ---------------- Run App ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
