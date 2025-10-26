
import os
import qrcode
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import io

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize Firebase
cred = credentials.Certificate(os.getenv("FIREBASE_ADMIN_SDK_JSON"))
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/generate_qr', methods=['GET'])
def generate_qr():
    """
    Generates a QR code for a given course ID.
    Expects 'course_id' as a query parameter.
    """
    try:
        course_id = request.args.get('course_id')
        if not course_id:
            return jsonify({"success": False, "error": "course_id is required"}), 400

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(course_id)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Save the image to a in-memory file
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        app.logger.error(f"Error generating QR code: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    """
    Marks attendance for a student.
    Expects a JSON payload with 'student_id' and 'course_id'.
    """
    try:
        data = request.get_json()
        student_id = data['student_id']
        course_id = data['course_id']

        # Create a new attendance record
        attendance_ref, _ = db.collection('attendance').add({
            'student_id': student_id,
            'course_id': course_id,
            'timestamp': firestore.SERVER_TIMESTAMP
        })

        return jsonify({"success": True, "attendance_id": attendance_ref.id}), 201
    except Exception as e:
        app.logger.error(f"Error marking attendance: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/get_attendance', methods=['GET'])
def get_attendance():
    """
    Retrieves attendance records for a student.
    Expects 'student_id' as a query parameter.
    """
    try:
        student_id = request.args.get('student_id')
        if not student_id:
            return jsonify({"success": False, "error": "student_id is required"}), 400

        attendance_query = db.collection('attendance').where('student_id', '==', student_id).stream()
        attendance_records = [record.to_dict() for record in attendance_query]

        return jsonify({"success": True, "attendance": attendance_records}), 200
    except Exception as e:
        app.logger.error(f"Error getting attendance: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
