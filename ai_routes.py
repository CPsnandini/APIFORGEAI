import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import SavedEndpoint
from gemini_client import ask_gemini

ai_bp = Blueprint("ai", __name__, url_prefix="/ai")


def _get_owned_endpoint(endpoint_id, user_id):
    return SavedEndpoint.query.filter_by(id=endpoint_id, user_id=user_id).first()


@ai_bp.route("/generate-docs/<int:endpoint_id>", methods=["POST"])
@jwt_required()
def generate_docs(endpoint_id):
    user_id = int(get_jwt_identity())
    endpoint = _get_owned_endpoint(endpoint_id, user_id)
    if not endpoint:
        return jsonify({"error": "endpoint not found"}), 404

    headers = json.loads(endpoint.headers) if endpoint.headers else {}
    body = json.loads(endpoint.body) if endpoint.body else None

    prompt = f"""You are a technical writer. Write concise, professional API documentation
for the following endpoint, in Markdown format. Include: a one-line summary,
request method and URL, required headers, request body shape (if any),
and a likely example success response.

Method: {endpoint.method}
URL: {endpoint.url}
Headers: {json.dumps(headers)}
Body: {json.dumps(body) if body else "none"}
"""

    try:
        docs = ask_gemini(prompt)
    except Exception as e:
        return jsonify({"error": f"AI generation failed: {str(e)}"}), 502

    return jsonify({"endpoint_id": endpoint.id, "documentation": docs}), 200


@ai_bp.route("/explain-error", methods=["POST"])
@jwt_required()
def explain_error():
    data = request.get_json(silent=True) or {}
    status_code = data.get("status_code")
    response_body = data.get("response_body", "")

    if status_code is None:
        return jsonify({"error": "status_code is required"}), 400

    prompt = f"""You are an API debugging assistant. Explain this HTTP error to a developer
in plain language: what it likely means, the most common causes, and 2-3 concrete
things to check or try next.

HTTP Status Code: {status_code}
Response Body: {response_body}
"""

    try:
        explanation = ask_gemini(prompt)
    except Exception as e:
        return jsonify({"error": f"AI generation failed: {str(e)}"}), 502

    return jsonify({"status_code": status_code, "explanation": explanation}), 200


@ai_bp.route("/generate-tests/<int:endpoint_id>", methods=["POST"])
@jwt_required()
def generate_tests(endpoint_id):
    user_id = int(get_jwt_identity())
    endpoint = _get_owned_endpoint(endpoint_id, user_id)
    if not endpoint:
        return jsonify({"error": "endpoint not found"}), 404

    headers = json.loads(endpoint.headers) if endpoint.headers else {}
    body = json.loads(endpoint.body) if endpoint.body else None

    prompt = f"""You are a QA engineer. Generate 5 test cases for the following API endpoint.
Cover one happy-path success case, and several edge/failure cases (missing
fields, invalid auth, wrong method, malformed input). For each test case give:
a short name, the expected status code, and a one-line description of what it checks.
Return ONLY a JSON array of objects with keys: name, expected_status, description.
Do not include any text outside the JSON array.

Method: {endpoint.method}
URL: {endpoint.url}
Headers: {json.dumps(headers)}
Body: {json.dumps(body) if body else "none"}
"""

    try:
        raw = ask_gemini(prompt)
    except Exception as e:
        return jsonify({"error": f"AI generation failed: {str(e)}"}), 502

    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()

    try:
        test_cases = json.loads(cleaned)
    except json.JSONDecodeError:
        test_cases = raw

    return jsonify({"endpoint_id": endpoint.id, "test_cases": test_cases}), 200