from . import get_connection

def create_feedback_table():
    db = get_connection()
    if not db: return
    connection, cursor = db

    sql = """CREATE TABLE IF NOT EXISTS reviews  (
        review_id INT PRIMARY KEY,
        user_id VARCHAR(20),
        isDeleted INT NOT NULL,
        product_id INT,
        rating INT NOT NULL,
        feedback TEXT
    )"""

    cursor.execute(sql)
    connection.commit()
    print("TABLE CREATED!")
    connection.close()