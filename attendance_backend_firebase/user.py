from flask import Blueprint, request, jsonify
from firebase_admin import auth, firestore
from functools import wraps

user_bp = Blueprint("user", __name__)
db = firestore.client()

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return jsonify({"message": "Missing token"}), 401
        try:
            decoded = auth.verify_id_token(token)
            request.user = decoded
        except Exception as e:
            return jsonify({"message": f"Invalid token: {e}"}), 403
        return f(*args, **kwargs)
    return wrapper

@user_bp.route("/user", methods=["GET"])
@token_required
def get_user():
    user = request.user
    uid = user["uid"]
    try:
        user_record = auth.get_user(uid)
        user_data = {
            "uid": user_record.uid,
            "email": user_record.email,
            "display_name": user_record.display_name,
            "photo_url": user_record.photo_url
        }
        return jsonify(user_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@user_bp.route("/user", methods=["PUT"])
@token_required
def update_user():
    user = request.user
    uid = user["uid"]
    data = request.json
    try:
        updated_user = auth.update_user(
            uid,
            display_name=data.get("display_name"),
            photo_url=data.get("photo_url")
        )
        user_data = {
            "uid": updated_user.uid,
            "email": updated_user.email,
            "display_name": updated_user.display_name,
            "photo_url": updated_user.photo_url
        }
        return jsonify(user_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400