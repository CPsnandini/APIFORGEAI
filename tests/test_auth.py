import requests

BASE = "http://127.0.0.1:5000"

# 1. Signup
r = requests.post(f"{BASE}/auth/signup", json={"username": "testuser", "password": "testpass123"})
print("SIGNUP:", r.status_code, r.json())

# 2. Login
r = requests.post(f"{BASE}/auth/login", json={"username": "testuser", "password": "testpass123"})
print("LOGIN:", r.status_code, r.json())
token = r.json().get("access_token")

# 3. Protected route, using the token from step 2
r = requests.get(f"{BASE}/auth/me", headers={"Authorization": f"Bearer {token}"})
print("ME:", r.status_code, r.json())