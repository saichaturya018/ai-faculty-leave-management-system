from flask import Blueprint, request, jsonify
from config import db, cursor

leave_bp = Blueprint('leave', __name__)
@leave_bp.route('/apply_leave', methods=['POST'])
def apply_leave():

    data = request.json

    query = """
    INSERT INTO LeaveRequests
    (faculty_id, from_date, to_date, reason, status)
    VALUES (%s,%s,%s,%s,%s)
    """

    values = (
        data['faculty_id'],
        data['from_date'],
        data['to_date'],
        data['reason'],
        'Pending'
    )

    cursor.execute(query, values)
    db.commit()

    return jsonify({
        "message": "Leave Request Submitted Successfully"
    })
@leave_bp.route('/leave_history/<int:faculty_id>')
def leave_history(faculty_id):

    query = """
    SELECT *
    FROM LeaveRequests
    WHERE faculty_id=%s
    """

    cursor.execute(query, (faculty_id,))
    data = cursor.fetchall()

    return jsonify(data)
@leave_bp.route('/approve_leave/<int:leave_id>', methods=['PUT'])
def approve_leave(leave_id):

    query = """
    UPDATE LeaveRequests
    SET status='Approved'
    WHERE leave_id=%s
    """

    cursor.execute(query, (leave_id,))
    db.commit()

    return jsonify({
        "message":"Leave Approved"
    })
@leave_bp.route('/reject_leave/<int:leave_id>', methods=['PUT'])
def reject_leave(leave_id):

    query = """
    UPDATE LeaveRequests
    SET status='Rejected'
    WHERE leave_id=%s
    """

    cursor.execute(query, (leave_id,))
    db.commit()

    return jsonify({
        "message":"Leave Rejected"
    })

