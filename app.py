from flask import Flask, request, Response, jsonify, render_template_string
import requests
from urllib.parse import urljoin

app = Flask(__name__)

# SAFETY: only allow whitelisted upstreams for demos
ALLOWED_TARGETS = {"https://httpbin.org"}
TARGET = "https://httpbin.org"  # demo target

def scrub_headers(hdrs: dict) -> dict:
    blocked = {"authorization", "cookie", "set-cookie"}
    return {k: v for k, v in hdrs.items() if k.lower() not in blocked}

@app.route("/")
def home():
    return render_template_string("""
    <h1>SocialCyber Demo Proxy</h1>
    <p>Forward requests safely to <code>{{target}}</code>.</p>
    <ul>
      <li><a href="/proxy/get">/proxy/get</a> — forwards to httpbin.org/get</li>
      <li><a href="/_edu/inspect">/_edu/inspect</a> — see request details</li>
      <li><a href="/_edu/form">/_edu/form</a> — demo form POST</li>
    </ul>
    <p>Safe, educational, and clone-friendly.</p>
    """, target=TARGET)

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

@app.route("/_edu/form", methods=["GET"])
def demo_form():
    return render_template_string("""
    <h2>Demo Form</h2>
    <form action="/proxy/post" method="post">
      <label>Username: <input name="username"></label><br/>
      <label>Password: <input name="password" type="password"></label><br/>
      <button type="submit">Submit</button>
    </form>
    <p>Posts to httpbin.org safely.</p>
    """)

@app.route("/proxy/", defaults={"path": ""}, methods=["GET","POST"])
@app.route("/proxy/<path:path>", methods=["GET","POST"])
def proxy(path):
    if TARGET not in ALLOWED_TARGETS:
        return jsonify({"error": "Target not allowed"}), 400

    upstream_url = urljoin(TARGET + "/", path)
    req_headers = {k: v for k, v in request.headers if k.lower() != "host"}
    data = request.get_data()

    print(f"{request.method} {upstream_url}")
    print("Headers:", scrub_headers(dict(request.headers)))

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
    response_headers = [(k, v) for k, v in resp.headers.items() if k.lower() not in excluded]
    response_headers.append(("X-SocialCyber", "true"))

    return Response(resp.content, status=resp.status_code, headers=response_headers)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
