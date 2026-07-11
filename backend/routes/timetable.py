@timetable_bp.route('/updated_timetable')
def updated_timetable():

    query = "SELECT * FROM Timetable"

    cursor.execute(query)

    data = cursor.fetchall()

    return jsonify(data)