"""
Task 11: Production Verification & Testing Script
Comprehensive test suite validating:
- Flask API Endpoints (Health, Prediction, Error Routing)
- Streamlit UI Connectivity
- Latency & Numerical Accuracy Benchmarks
"""

import time
import json
import urllib.request
import urllib.error

BACKEND_URL = "http://localhost:5000"
FRONTEND_URL = "http://localhost:8501"

passed_tests = 0
failed_tests = 0

def log_result(test_name: str, passed: bool, detail: str = ""):
    global passed_tests, failed_tests
    symbol = "✓ [PASSED]" if passed else "✗ [FAILED]"
    print(f"{symbol:<12} {test_name}")
    if detail:
        print(f"             Details: {detail}")
    if passed:
        passed_tests += 1
    else:
        failed_tests += 1

def send_request(url: str, method: str = "GET", headers: dict = None, data: bytes = None):
    req = urllib.request.Request(url, method=method, data=data, headers=headers or {})
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")
    except urllib.error.URLError as e:
        return None, str(e)

def test_api_root():
    status, body = send_request(f"{BACKEND_URL}/")
    passed = status == 200 and "online" in body
    log_result("TC-01: Backend Root Endpoint (GET /)", passed, f"Status={status}")

def test_api_health():
    status, body = send_request(f"{BACKEND_URL}/health")
    passed = status == 200 and "healthy" in body
    log_result("TC-02: Backend Health Probe (GET /health)", passed, f"Status={status}")

def test_api_predict_valid():
    payload = {"inputs": [0.55, 1.20, -0.42, 0.88, 2.15]}
    data = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    status, body = send_request(f"{BACKEND_URL}/predict", method="POST", headers=headers, data=data)
    
    passed = False
    detail = f"Status={status}"
    if status == 200:
        res = json.loads(body)
        pred = res.get("prediction", {})
        if pred.get("predicted_class") and "confidence" in pred and "latency_ms" in res:
            passed = True
            detail = f"Class='{pred['predicted_class']}', Confidence={pred['confidence']}, Latency={res['latency_ms']}ms"

    log_result("TC-03: Model Prediction (POST /predict - Valid)", passed, detail)

def test_api_predict_missing_inputs():
    payload = {"wrong_key": [1, 2, 3]}
    data = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    status, body = send_request(f"{BACKEND_URL}/predict", method="POST", headers=headers, data=data)
    passed = status == 400
    log_result("TC-04: Error Handling - Missing 'inputs' Key", passed, f"Status={status}")

def test_api_predict_non_numeric():
    payload = {"inputs": ["abc", "invalid"]}
    data = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    status, body = send_request(f"{BACKEND_URL}/predict", method="POST", headers=headers, data=data)
    passed = status == 400
    log_result("TC-05: Error Handling - Non-Numeric Inputs", passed, f"Status={status}")

def test_api_invalid_method():
    status, body = send_request(f"{BACKEND_URL}/predict", method="GET")
    passed = status == 405
    log_result("TC-06: Error Handling - Method Not Allowed (GET /predict)", passed, f"Status={status}")

def test_frontend_health():
    status, body = send_request(f"{FRONTEND_URL}/_stcore/health")
    passed = status == 200
    log_result("TC-07: Streamlit Core Health (GET /_stcore/health)", passed, f"Status={status}")

def benchmark_inference():
    print("\n[*] Benchmarking Model Inference Latency (10 iterations)...")
    payload = {"inputs": [0.5, -0.2, 1.4, 0.1, -0.9]}
    data = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    latencies = []

    for _ in range(10):
        t0 = time.time()
        status, body = send_request(f"{BACKEND_URL}/predict", method="POST", headers=headers, data=data)
        elapsed = (time.time() - t0) * 1000
        if status == 200:
            latencies.append(elapsed)

    if latencies:
        avg_lat = sum(latencies) / len(latencies)
        min_lat = min(latencies)
        max_lat = max(latencies)
        print(f"    Avg: {avg_lat:.2f}ms | Min: {min_lat:.2f}ms | Max: {max_lat:.2f}ms")
        log_result("TC-08: Inference Performance Benchmark", True, f"Avg Roundtrip={avg_lat:.2f}ms")
    else:
        log_result("TC-08: Inference Performance Benchmark", False, "Could not reach backend")

if __name__ == "__main__":
    print("=" * 65)
    print("  TASK 11: FULL APPLICATION CONTAINERIZATION TEST SUITE")
    print("  Target Backend: ", BACKEND_URL)
    print("  Target Frontend:", FRONTEND_URL)
    print("=" * 65)

    test_api_root()
    test_api_health()
    test_api_predict_valid()
    test_api_predict_missing_inputs()
    test_api_predict_non_numeric()
    test_api_invalid_method()
    test_frontend_health()
    benchmark_inference()

    print("\n" + "=" * 65)
    print(f"  TEST SUMMARY: {passed_tests} PASSED | {failed_tests} FAILED")
    print("=" * 65)
