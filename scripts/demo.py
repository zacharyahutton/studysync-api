import json
import urllib.request

BASE = "http://127.0.0.1:8000"

def post(path, body):
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        return json.loads(resp.read().decode())

if __name__ == "__main__":
    try:
        post("/auth/register", {"email": "demo@studysync.local", "password": "password123"})
    except Exception:
        pass
    print(json.dumps(post("/auth/login", {"email": "demo@studysync.local", "password": "password123"}), indent=2))
