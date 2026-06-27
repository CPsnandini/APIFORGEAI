import requests

BASE = "http://127.0.0.1:5000"

# ---------- DAY 1: AUTH ----------
r = requests.post(f"{BASE}/auth/signup", json={"username": "testuser", "password": "testpass123"})
print("SIGNUP:", r.status_code, r.json())

r = requests.post(f"{BASE}/auth/login", json={"username": "testuser", "password": "testpass123"})
print("LOGIN:", r.status_code, r.json())
token = r.json().get("access_token")
headers = {"Authorization": f"Bearer {token}"}

r = requests.get(f"{BASE}/auth/me", headers=headers)
print("ME:", r.status_code, r.json())

r = requests.post(f"{BASE}/api/send", headers=headers, json={
    "method": "GET", "url": "https://api.github.com/users/octocat"
})
print("SEND:", r.status_code, r.json()["status_code"], r.json()["duration_ms"], "ms")

r = requests.post(f"{BASE}/api/endpoints", headers=headers, json={
    "name": "GitHub octocat profile", "method": "GET",
    "url": "https://api.github.com/users/octocat"
})
print("SAVE ENDPOINT:", r.status_code, r.json())
endpoint_id = r.json()["id"]

r = requests.get(f"{BASE}/api/endpoints", headers=headers)
print("LIST ENDPOINTS:", r.status_code, len(r.json()), "saved")

r = requests.get(f"{BASE}/api/history", headers=headers)
print("HISTORY:", r.status_code, len(r.json()), "entries")

r = requests.post(f"{BASE}/api/send", headers=headers, json={"method": "FOO", "url": "https://api.github.com"})
print("BAD METHOD (expect 400):", r.status_code, r.json())

r = requests.post(f"{BASE}/ai/generate-docs/{endpoint_id}", headers=headers)
print("GENERATE DOCS:", r.status_code)
print(r.json().get("documentation", r.json()))

r = requests.post(f"{BASE}/ai/explain-error", headers=headers, json={
    "status_code": 404, "response_body": '{"error": "user not found"}'
})
print("\nEXPLAIN ERROR:", r.status_code)
print(r.json().get("explanation", r.json()))

r = requests.post(f"{BASE}/ai/generate-tests/{endpoint_id}", headers=headers)
print("\nGENERATE TESTS:", r.status_code)
print(r.json().get("test_cases", r.json()))