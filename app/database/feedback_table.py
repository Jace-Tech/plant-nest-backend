from . import get_connection

def create_feedback_table():
    db = get_connection()
    if not db: return
    connection, cursor = db

    sql = """CREATE TABLE IF NOT EXISTS reviews (
        review_id INT PRIMARY KEY AUTO_INCREMENT,
        user_id VARCHAR(20),
        product_id VARCHAR(20),
        rating INT NOT NULL,
        feedback TEXT,
        `date` DATETIME
    )"""

    cursor.execute(sql)
    connection.commit()
    print("TABLE CREATED!")
    connection.close()




def get_all_reviews():
	"""Returns all the reviews"""

	db = get_connection()
	if not db: return
	_, cursor = db
	sql = "SELECT * FROM reviews"

	cursor.execute(sql)
	return cursor.fetchall()
