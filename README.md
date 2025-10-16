# Backend for Automated Attendance System

This directory contains the Python backend for the Automated Attendance System. It uses Flask to create a web server and connects to Firebase for database and authentication services.

## Setup and Installation

### 1. Install Dependencies

Install all the necessary Python packages using pip:

```bash
pip install -r requirements.txt
```

### 2. Configure Firebase

1.  **Download your Firebase service account key:**
    *   Go to your Firebase project console.
    *   Navigate to **Project settings** > **Service accounts**.
    *   Click on **Generate new private key** and download the JSON file.

2.  **Save the key:**
    *   Rename the downloaded file to `serviceAccountKey.json`.
    *   Place it in the `attendance-backend` directory (the same directory as this README).

### 3. Set Environment Variables

Create a `.env` file in the `attendance-backend` directory by copying the example file:

```bash
cp .env.example .env
```

The `.env` file should contain the following:

```
FIREBASE_CREDENTIAL_PATH=serviceAccountKey.json
PORT=5000
```

## Running the Server

Once you have completed the setup, you can run the backend server:

```bash
python attendance-backend/attendance_backend_firebase/app.py
```

You should see a message indicating that the server is running on port 5000 and whether the Firebase Admin SDK was initialized successfully.

### Verify Server Startup

To confirm that the server is running, you can send a GET request to the `/ping` endpoint:

```bash
curl http://localhost:5000/ping
```

You should receive the following response:

```json
{
  "message": "pong!"
}
```
