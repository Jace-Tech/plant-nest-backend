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
		`password` VARCHAR(255) NOT NULL
	)"""

	cursor.execute(sql)
	connection.commit()
	print("TABLE CREATED!")
	connection.close()
