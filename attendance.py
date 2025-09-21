from flask import Blueprint, request, jsonify
from db import get_db
import jwt, os
from functools import wraps
attendance_bp = Blueprint("attendance", __name__)
def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None
		if "Authorization" in request.headers:
			token = request.headers["Authorization"].split(" ")[1]
		if not token:
			return jsonify({"message": "Token missing"}), 401
		try:
			data = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
			request.user = data
		except Exception:
			return jsonify({"message": "Token invalid"}), 403
		return f(*args, **kwargs)
	return decorated
@attendance_bp.route("/attendance", methods=["POST"])
@token_required
def mark_attendance():
	data = request.json
	conn = get_db()
	cur = conn.cursor()
	student_id = data.get("student_id") or request.user["id"]
	note = data.get("note")
	cur.execute("INSERT INTO attendance (student_id, note) VALUES (%s, %s)", (student_id, note))
@attendance_bp.route("/attendance", methods=["GET"])
@token_required
def get_attendance():
	student_id = request.args.get("student_id") or request.user["id"]
	conn = get_db()
	cur = conn.cursor()
	cur.execute("SELECT a.id, u.name, u.email, a.timestamp, a.note FROM attendance a JOIN users u ON a.student_id = u.id WHERE a.student_id = %s", (student_id,))
	rows = cur.fetchall()
	return jsonify(rows)