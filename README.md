# Attendance Backend

This is the backend for the Automated Attendance System, built with Flask.

## Setup

1.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Create a `.env` file** and add the following:

    ```
    FIREBASE_ADMIN_SDK_JSON=<path to your serviceAccountKey.json>
    ```

3.  **Run the server:**

    ```bash
    python app.py
    ```

## API Endpoints

*   `POST /mark_attendance`

    *   Marks attendance for a student.
    *   **Request Body:** `{"student_id": "<student_id>", "course_id": "<course_id>"}`
    *   **Response:** `{"success": true, "attendance_id": "<attendance_id>"}`

*   `GET /get_attendance`

    *   Retrieves attendance records for a student.
    *   **Query Parameters:** `student_id=<student_id>`
    *   **Response:** `{"success": true, "attendance": [...]}`
