from . import get_connection

def create_feedback_table():
    db = get_connection()
    if not db: return
    connection, cursor = db

    sql = """CREATE TABLE reviews (
        review_id INT PRIMARY KEY,
        user_id VARCHAR(20),
        product_id INT,
        rating INT NOT NULL,
        feedback TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (product_id) REFERENCES plants(plant_id)
    )"""

    cursor.execute(sql)
    connection.commit()
    print("TABLE CREATED!")
    connection.close()