from . import get_connection
from datetime import datetime


def create_feedback_table():
    db = get_connection()
    if not db:
        return
    
    connection, cursor = db

    sql = """CREATE TABLE IF NOT EXISTS feedback (
        feedback_id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(50),
        email VARCHAR(100),
        message TEXT,
        date DATETIME
    )"""

    cursor.execute(sql)
    connection.commit()
    print("FEEDBACK TABLE CREATED!")
    connection.close()
