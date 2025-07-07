from .db import get_connection

def check_user_credentials(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM admin WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None