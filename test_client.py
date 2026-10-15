"""
Verification Script for Flask Deep Learning API Container
Tests healthcheck and inference (/predict) endpoints.
"""
import json
import urllib.request
import urllib.error
import time

BASE_URL = "http://localhost:5000"

def test_health():
    print("[*] Testing GET /health ...")
    try:
        req = urllib.request.Request(f"{BASE_URL}/health", method="GET")
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"[+] Status: {resp.status}")
            print(f"[+] Response: {json.dumps(data, indent=2)}")
            assert resp.status == 200
            print("[✓] Health Check PASSED\n")
    except urllib.error.URLError as e:
        print(f"[X] Connection failed: {e}. Is the container running?")
        return False
    return True

def test_prediction():
    print("[*] Testing POST /predict ...")
    payload = {
        "inputs": [0.55, 1.20, -0.42, 0.88, 2.15]
    }
    encoded_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/predict",
        data=encoded_data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"[+] Status: {resp.status}")
            print(f"[+] Response:\n{json.dumps(data, indent=2)}")
            assert resp.status == 200
            assert data.get("status") == "success"
            print("\n[✓] Inference Test PASSED")
    except urllib.error.URLError as e:
        print(f"[X] Prediction request failed: {e}")
        return False
    return True

if __name__ == "__main__":
    print("=" * 60)
    print(" FLASK DEEP LEARNING API - CONTAINER VERIFICATION TEST")
    print("=" * 60)
    if test_health():
        test_prediction()
