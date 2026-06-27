import requests

BASE = "http://127.0.0.1:5000"

# ---------- DAY 1: AUTH ----------

# 1. Signup
r = requests.post(f"{BASE}/auth/signup", json={"username": "testuser", "password": "testpass123"})
print("SIGNUP:", r.status_code, r.json())

# 2. Login
r = requests.post(f"{BASE}/auth/login", json={"username": "testuser", "password": "testpass123"})
print("LOGIN:", r.status_code, r.json())
token = r.json().get("access_token")
headers = {"Authorization": f"Bearer {token}"}

# 3. Protected route, using the token from step 2
r = requests.get(f"{BASE}/auth/me", headers=headers)
print("ME:", r.status_code, r.json())


# 4. Send a real GET request through your engine, to a real public API
r = requests.post(f"{BASE}/api/send", headers=headers, json={
    "method": "GET",
    "url": "https://api.github.com/users/octocat"
})
print("SEND:", r.status_code, r.json()["status_code"], r.json()["duration_ms"], "ms")

# 5. Save an endpoint
r = requests.post(f"{BASE}/api/endpoints", headers=headers, json={
    "name": "GitHub octocat profile",
    "method": "GET",
    "url": "https://api.github.com/users/octocat"
})
print("SAVE ENDPOINT:", r.status_code, r.json())

# 6. List saved endpoints
r = requests.get(f"{BASE}/api/endpoints", headers=headers)
print("LIST ENDPOINTS:", r.status_code, len(r.json()), "saved")

# 7. Check history got logged from step 4
r = requests.get(f"{BASE}/api/history", headers=headers)
print("HISTORY:", r.status_code, len(r.json()), "entries")

# 8. Error case — bad method should be rejected before any request is sent
r = requests.post(f"{BASE}/api/send", headers=headers, json={"method": "FOO", "url": "https://api.github.com"})
print("BAD METHOD (expect 400):", r.status_code, r.json())