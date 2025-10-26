from flask import Blueprint, request, jsonify
from firebase_admin import auth
auth_bp = Blueprint("auth", __name__)
@auth_bp.route("/register", methods=["POST"])
def register():
 data = request.json
 try:
  user = auth.create_user(
  email=data["email"],
  password=data["password"],
  display_name=data.get("name", "")
  )
  return jsonify({"uid": user.uid, "email": user.email, "name": user.display_name})
 except Exception as e:
  return jsonify({"error": str(e)}), 400
