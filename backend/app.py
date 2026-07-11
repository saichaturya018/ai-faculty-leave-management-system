from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# -------------------------------------------------------------------------
# Database Connection
# -------------------------------------------------------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="A24126551002@Sai",
        database="faculty_leave"
    )

# -------------------------------------------------------------------------
# Direct Routes (No Blueprints Needed)
# -------------------------------------------------------------------------
@app.route('/apply_leave', methods=['POST'])
def apply_leave():
    data = request.get_json()
    
    # 1. Extract fields from the incoming JSON request
    # Make sure these match the keys you send from the frontend/browser console
    faculty_id = data.get('faculty_id')
    leave_type = data.get('leave_type')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    reason = data.get('reason')
    
    # Quick validation check
    if not all([faculty_id, leave_type, start_date, end_date]):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    db = None
    cursor = None
    
    try:
        # 2. Connect to the database
        db = get_connection()
        cursor = db.cursor()
        
        # 3. Write your SQL Insert Query
        # (Change table_name and column names to match your actual database schema)
        query = """
            INSERT INTO leave_applications (faculty_id, leave_type, start_date, end_date, reason, status)
            VALUES (%s, %s, %s, %s, %s, 'Pending')
        """
        values = (faculty_id, leave_type, start_date, end_date, reason)
        
        # 4. Execute and Commit the transaction
        cursor.execute(query, values)
        db.commit() 
        
        return jsonify({
            "status": "success", 
            "message": "Leave application submitted successfully!",
            "application_id": cursor.lastrowid
        }), 201

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return jsonify({"status": "error", "message": "Database insertion failed"}), 500
        
    finally:
        # 5. Clean up and close connections safely
        if cursor:
            cursor.close()
        if db:
            db.close()

# Quick test route to make sure backend is up
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Backend is running fine!"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
@app.route('/leave_history/<int:faculty_id>', methods=['GET'])
def get_leave_history(faculty_id):
    db = get_connection()
    if not db:
        return jsonify({"status": "error", "message": "Database connection failed"}), 500
        
    try:
        cursor = db.cursor(dictionary=True)
        # Fetching all leave requests submitted by this specific faculty member
        query = """
            SELECT leave_id, leave_date, reason, status 
            FROM leave_request 
            WHERE faculty_id = %s 
            ORDER BY leave_date DESC
        """
        cursor.execute(query, (faculty_id,))
        history = cursor.fetchall()
        
        return jsonify({
            "status": "success",
            "faculty_id": faculty_id,
            "history": history
        }), 200
        
    except mysql.connector.Error as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        db.close()
@app.route('/faculty/timetable/<int:faculty_id>/<string:day>', methods=['GET'])
def get_faculty_schedule(faculty_id, day):
    db = get_connection()
    if not db:
        return jsonify({"status": "error", "message": "Database connection failed"}), 500
        
    try:
        cursor = db.cursor(dictionary=True)
        # Fetch periods for the faculty on a specific day (e.g., 'Monday')
        query = """
            SELECT timetable_id, period, subject 
            FROM timetable 
            WHERE faculty_id = %s AND day = %s
            ORDER BY period ASC
        """
        cursor.execute(query, (faculty_id, day))
        schedule = cursor.fetchall()
        
        return jsonify({"status": "success", "schedule": schedule}), 200
    except mysql.connector.Error as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        db.close()
