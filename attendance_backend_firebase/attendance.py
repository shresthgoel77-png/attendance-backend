from flask import Blueprint, request, jsonify
from firebase_admin import firestore, auth
from functools import wraps
attendance_bp = Blueprint("attendance", __name__)
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
@attendance_bp.route("/attendance", methods=["POST"])
@token_required
def mark_attendance():
 data = request.json
 user = request.user
 record = {
 "user_id": user["uid"],
 "email": user["email"],
 "timestamp": firestore.SERVER_TIMESTAMP,
 "note": data.get("note", "")
 }
 db.collection("attendance").add(record)
 return jsonify({"message": "Attendance marked successfully"})
@attendance_bp.route("/attendance", methods=["GET"])
@token_required
def get_attendance():
 user = request.user
 docs = db.collection("attendance").where("user_id", "==", user["uid"]).stream()
 records = [doc.to_dict() for doc in docs]
 return jsonify(records)