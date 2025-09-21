from flask import Blueprint, request, jsonify
from db import get_db
import bcrypt, jwt, datetime, os
from dotenv import load_dotenv
load_dotenv()
auth_bp = Blueprint("auth", __name__)
@auth_bp.route("/register", methods=["POST"])
def register():
	data = request.json
	conn = get_db()
	cur = conn.cursor()
	hashed = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt())
	try:
		cur.execute(
			"INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
			(data.get("name"), data["email"], hashed, data.get("role", "student"))
		)
		conn.commit()
	except Exception as e:
		return jsonify({"message": "Email already exists"}), 409
	token = jwt.encode({
		"email": data["email"],
		"role": data.get("role", "student"),
		"exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
	}, os.getenv("JWT_SECRET"), algorithm="HS256")
	return jsonify({"token": token})

@auth_bp.route("/login", methods=["POST"])
def login():
	data = request.json
	conn = get_db()
	cur = conn.cursor()
	cur.execute("SELECT id, name, email, password, role FROM users WHERE email=%s", (data["email"],))
	user = cur.fetchone()
	if not user or not bcrypt.checkpw(data["password"].encode("utf-8"), user[3].encode("utf-8")):
		return jsonify({"message": "Invalid credentials"}), 401
	token = jwt.encode({
		"id": user[0],
		"email": user[2],
		"role": user[4],
		"exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
	}, os.getenv("JWT_SECRET"), algorithm="HS256")
	return jsonify({
		"token": token,
		"user": {
			"id": user[0],
			"name": user[1],
			"email": user[2],
			"role": user[4]
		}
	})