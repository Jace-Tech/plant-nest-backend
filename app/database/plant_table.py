from . import get_connection

def create_plant_table():
	db = get_connection()

	if not db: return

	connection, cursor = db
	sql = """CREATE TABLE IF NOT EXISTS plants (
		`plant_id` VARCHAR(20) PRIMARY KEY,
		`name` VARCHAR(50), 
		`description` TEXT,
		`price` FLOAT,
		`quantity` INT,
		`image_url` LONGTEXT,
		`is_available` TINYINT DEFAULT 1,
		`category_id` VARCHAR(20),
		`date` DATETIME
	)"""

	cursor.execute(sql)
	connection.commit()
	print("TABLE CREATED!")
	connection.close()


def get_all_plants():
	"""Returns all the plants, togther with the category"""

	db = get_connection()
	if not db: return
	_, cursor = db
	sql = """
		SELECT P.*, C.name AS category_name 
		FROM plants AS P 
		INNER JOIN categories AS C 
		ON P.category_id = C.category_id"""

	cursor.execute(sql)
	return cursor.fetchall()


def get_one_plant(id):
	db = get_connection()
	if not db: return
	_, cursor = db
	sql = """
		SELECT P.*, C.name AS category_name 
		FROM plants AS P 
		INNER JOIN categories AS C 
		ON P.category_id = C.category_id WHERE plant_id = %s"""

	cursor.execute(sql, [id])
	return cursor.fetchone()
