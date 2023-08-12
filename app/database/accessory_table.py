from . import get_connection

def create_accessory_table():
	db = get_connection()

	if not db: return

	connection, cursor = db
	sql = """CREATE TABLE IF NOT EXISTS accessories (
		`accessory_id` VARCHAR(20) PRIMARY KEY,
		`name` VARCHAR(50), 
		`description` TEXT,
		`price` FLOAT,
		`quantity` INT,
		`image_url` VARCHAR(200),
		`is_available` TINYINT DEFAULT 1
	)"""

	cursor.execute(sql)
	connection.commit()
	print("TABLE CREATED!")
	connection.close()


def get_all_accessories():
	"""Returns all the accessories"""

	db = get_connection()
	if not db: return
	_, cursor = db
	sql = """ SELECT * FROM accessories """

	cursor.execute(sql)
	return cursor.fetchall()


def get_one_accessory(id):
	db = get_connection()
	if not db: return
	_, cursor = db
	sql = "SELECT * FROM accessories WHERE accessory_id = %s"

	cursor.execute(sql, [id])
	return cursor.fetchone()
