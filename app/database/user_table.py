from . import get_connection

def create_user_table():
	db = get_connection()

	if not db: return

	connection, cursor = db
	sql = """CREATE TABLE IF NOT EXISTS `users` (
		`user_id` VARCHAR(20) PRIMARY KEY,
		`fullname` VARCHAR(50), 
		`username` VARCHAR(50),
		`contact_number` VARCHAR(15) DEFAULT NULL,
		`email` VARCHAR(100) UNIQUE NOT NULL,
		`password` VARCHAR(255) NOT NULL,
		`date` DATETIME
	)"""

	cursor.execute(sql)
	connection.commit()
	print("TABLE CREATED!")
	connection.close()



def get_all_users():
	"""Returns all the users"""

	db = get_connection()
	if not db: return
	_, cursor = db
	sql = "SELECT * FROM users"

	cursor.execute(sql)
	return cursor.fetchall()



def get_one_user(id):
	"""Returns one user"""

	db = get_connection()
	if not db: return
	_, cursor = db
	sql = "SELECT * FROM users WHERE user_id = %s"

	cursor.execute(sql, [id])
	return cursor.fetchone()

