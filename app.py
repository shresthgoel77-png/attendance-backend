from flask import Flask
from flask_cors import CORS
from auth import auth_bp
from attendance import attendance_bp
app = Flask(__name__)
CORS(app)
app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(attendance_bp, url_prefix="/api")
if __name__ == "__main__":
 app.run(debug=True, host="0.0.0.0", port=5000)