import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import SavedEndpoint, RequestHistory
from api_executor import execute_request

tester_bp = Blueprint("tester", __name__, url_prefix="/api")

ALLOWED_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE"}


@tester_bp.route("/send", methods=["POST"])
@jwt_required()
def send():
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}

    method = (data.get("method") or "GET").upper()
    url = data.get("url")
    headers = data.get("headers") or {}
    body = data.get("body")

    if not url:
        return jsonify({"error": "url is required"}), 400
    if method not in ALLOWED_METHODS:
        return jsonify({"error": f"method must be one of {sorted(ALLOWED_METHODS)}"}), 400

    result = execute_request(method, url, headers, body)

    history = RequestHistory(
        user_id=user_id,
        method=method,
        url=url,
        status_code=result.get("status_code"),
        response_snippet=result.get("response_text", "")[:2000],
        duration_ms=result.get("duration_ms"),
    )
    db.session.add(history)
    db.session.commit()

    return jsonify(result), 200


@tester_bp.route("/endpoints", methods=["POST"])
@jwt_required()
def create_endpoint():
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}

    name = data.get("name")
    method = (data.get("method") or "GET").upper()
    url = data.get("url")
    headers = data.get("headers") or {}
    body = data.get("body")

    if not name or not url:
        return jsonify({"error": "name and url are required"}), 400

    endpoint = SavedEndpoint(
        user_id=user_id,
        name=name,
        method=method,
        url=url,
        headers=json.dumps(headers),
        body=json.dumps(body) if body is not None else None,
    )
    db.session.add(endpoint)
    db.session.commit()

    return jsonify({"message": "endpoint saved", "id": endpoint.id}), 201


@tester_bp.route("/endpoints", methods=["GET"])
@jwt_required()
def list_endpoints():
    user_id = int(get_jwt_identity())
    endpoints = (SavedEndpoint.query
                 .filter_by(user_id=user_id)
                 .order_by(SavedEndpoint.created_at.desc())
                 .all())

    return jsonify([{
        "id": e.id,
        "name": e.name,
        "method": e.method,
        "url": e.url,
        "headers": json.loads(e.headers) if e.headers else {},
        "body": json.loads(e.body) if e.body else None,
        "created_at": e.created_at.isoformat(),
    } for e in endpoints]), 200


@tester_bp.route("/endpoints/<int:endpoint_id>", methods=["GET"])
@jwt_required()
def get_endpoint(endpoint_id):
    user_id = int(get_jwt_identity())
    e = SavedEndpoint.query.filter_by(id=endpoint_id, user_id=user_id).first()
    if not e:
        return jsonify({"error": "endpoint not found"}), 404

    return jsonify({
        "id": e.id, "name": e.name, "method": e.method, "url": e.url,
        "headers": json.loads(e.headers) if e.headers else {},
        "body": json.loads(e.body) if e.body else None,
        "created_at": e.created_at.isoformat(),
    }), 200


@tester_bp.route("/endpoints/<int:endpoint_id>", methods=["DELETE"])
@jwt_required()
def delete_endpoint(endpoint_id):
    user_id = int(get_jwt_identity())
    e = SavedEndpoint.query.filter_by(id=endpoint_id, user_id=user_id).first()
    if not e:
        return jsonify({"error": "endpoint not found"}), 404

    db.session.delete(e)
    db.session.commit()
    return jsonify({"message": "endpoint deleted"}), 200


@tester_bp.route("/history", methods=["GET"])
@jwt_required()
def get_history():
    user_id = int(get_jwt_identity())
    records = (RequestHistory.query
               .filter_by(user_id=user_id)
               .order_by(RequestHistory.created_at.desc())
               .limit(20)
               .all())

    return jsonify([{
        "id": r.id, "method": r.method, "url": r.url,
        "status_code": r.status_code, "response_snippet": r.response_snippet,
        "duration_ms": r.duration_ms, "created_at": r.created_at.isoformat(),
    } for r in records]), 200