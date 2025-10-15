from flask import Flask
from flask_cors import CORS
from firebase_admin import credentials, initialize_app
from auth import auth_bp
from attendance import attendance_bp
from user import user_bp
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
CORS(app)
cred = credentials.Certificate(os.getenv("FIREBASE_KEY_PATH"))
initialize_app(cred)
app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(attendance_bp, url_prefix="/api")
app.register_blueprint(user_bp, url_prefix="/api")
if __name__ == "__main__":
  app.run(debug=True, port=int(os.getenv("PORT", 5000)))