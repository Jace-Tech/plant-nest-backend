from . import get_connection

def create_category_table():
	db = get_connection()

	if not db: return

	connection, cursor = db
	sql = """CREATE TABLE IF NOT EXISTS categories (
		`category_id` VARCHAR(20) PRIMARY KEY,
		`name` VARCHAR(50)
	)"""

	cursor.execute(sql)
	connection.commit()
	print("TABLE CREATED!")
	connection.close()


def get_all_categories():
	db = get_connection()
	if not db: return
	_, cursor = db
	sql = "SELECT * FROM categories"
	cursor.execute(sql)
	return cursor.fetchall()


def get_category_by_id(id):
	db = get_connection()
	if not db: return
	_, cursor = db
	sql = "SELECT * FROM categories WHERE category_id = %s"
	cursor.execute(sql, [id])
	return cursor.fetchone()
