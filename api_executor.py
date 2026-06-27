import time
import requests

TIMEOUT_SECONDS = 10


def execute_request(method, url, headers=None, body=None):
    headers = headers or {}
    start = time.time()

    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=body if body is not None else None,
            timeout=TIMEOUT_SECONDS,
        )
        duration_ms = int((time.time() - start) * 1000)

        return {
            "status_code": response.status_code,
            "response_text": response.text,
            "response_headers": dict(response.headers),
            "duration_ms": duration_ms,
        }

    except requests.exceptions.Timeout:
        return {
            "status_code": None,
            "response_text": f"Request timed out after {TIMEOUT_SECONDS} seconds",
            "response_headers": {},
            "duration_ms": int((time.time() - start) * 1000),
        }

    except requests.exceptions.ConnectionError:
        return {
            "status_code": None,
            "response_text": "Could not connect to the target URL",
            "response_headers": {},
            "duration_ms": int((time.time() - start) * 1000),
        }

    except requests.exceptions.RequestException as e:
        return {
            "status_code": None,
            "response_text": f"Request failed: {str(e)}",
            "response_headers": {},
            "duration_ms": int((time.time() - start) * 1000),
        }