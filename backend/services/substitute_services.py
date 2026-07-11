def find_substitute(subject):

    query = """
    SELECT *
    FROM Faculty
    WHERE subject=%s
    ORDER BY workload ASC
    LIMIT 1
    """

    cursor.execute(query,(subject,))
    faculty = cursor.fetchone()

    return faculty