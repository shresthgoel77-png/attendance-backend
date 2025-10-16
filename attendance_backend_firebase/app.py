
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore, auth, storage
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# --- Firebase Initialization ---
try:
    cred_path = os.environ.get("FIREBASE_CREDENTIAL_PATH")
    if not cred_path:
        raise ValueError("FIREBASE_CREDENTIAL_PATH environment variable not set.")

    # Check if the file exists before creating credentials
    if not os.path.exists(cred_path):
         raise FileNotFoundError(f"Service account key file not found at: {cred_path}")

    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        '''storageBucket':''' # Add your storage bucket name here if you use Storage
    })
    db = firestore.client()
    print("Firebase Admin SDK initialized successfully.")

except (ValueError, FileNotFoundError) as e:
    print(f"Error initializing Firebase Admin SDK: {e}")
    print("Backend is running without Firebase connection. Some features may not work.")
    db = None # Set db to None if initialization fails


# --- Routes ---

@app.route("/ping", methods=['GET'])
def ping():
    """A simple test route to confirm the server is running."""
    return jsonify({"message": "pong!"}), 200

@app.route("/attendance", methods=['POST'])
def mark_attendance():
    """
    A placeholder route to demonstrate marking attendance.
    Expects a JSON payload with 'studentId' and 'status'.
    """
    if not db:
        return jsonify({"error": "Firestore is not connected."}), 500

    try:
        data = request.get_json()
        student_id = data.get('studentId')
        status = data.get('status')

        if not student_id or not status:
            return jsonify({"error": "Missing studentId or status in request."}), 400

        # Add attendance record to Firestore
        attendance_ref = db.collection('attendance').document()
        attendance_ref.set({
            'studentId': student_id,
            'status': status,
            'timestamp': firestore.SERVER_TIMESTAMP
        })

        return jsonify({"message": "Attendance marked successfully.", "doc_id": attendance_ref.id}), 201

    except Exception as e:
        print(f"Error in /attendance route: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500


@app.route("/attendance/<student_id>", methods=['GET'])
def get_attendance(student_id):
    """
    A placeholder route to retrieve attendance for a specific student.
    """
    if not db:
        return jsonify({"error": "Firestore is not connected."}), 500

    try:
        # Query Firestore for attendance records
        attendance_query = db.collection('attendance').where('studentId', '==', student_id).stream()

        records = []
        for record in attendance_query:
            records.append(record.to_dict())

        return jsonify({"studentId": student_id, "attendance": records}), 200

    except Exception as e:
        print(f"Error in /attendance/<student_id> route: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500


# --- Main Execution ---

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
