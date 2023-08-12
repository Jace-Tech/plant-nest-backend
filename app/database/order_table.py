from . import get_connection

def create_orders_table():
	db = get_connection()

	if not db: return

	connection, cursor = db
	sql = """CREATE TABLE IF NOT EXISTS `orders` (
		`order_id` VARCHAR(20) PRIMARY KEY,
		`user_id` VARCHAR(20),
        `firstname` VARCHAR(50),
        `lastname` VARCHAR(50),
        `phone` VARCHAR(15) DEFAULT NULL,
        `email` VARCHAR(100) DEFAULT NULL,
		`products` VARCHAR(255) NOT NULL,
		`address` VARCHAR(15) NOT NULL,
		`amount` FLOAT NOT NULL,
		`date` DATETIME
	)"""

	cursor.execute(sql)
	connection.commit()
	print("TABLE CREATED!")
	connection.close()


def get_all_orders():
	"""Returns all the orders"""

	db = get_connection()
	if not db: return
	_, cursor = db
	sql = "SELECT * FROM orders"

	cursor.execute(sql)
	return cursor.fetchall()

def get_users_order(user_id):
	"""Returns user's order"""

	db = get_connection()
	if not db: return
	_, cursor = db
	sql = "SELECT * FROM orders WHERE user_id = %s"

	cursor.execute(sql, [user_id])
	return cursor.fetchall()


def get_order_by_id(id):
	"""Returns one order"""

	db = get_connection()
	if not db: return
	_, cursor = db
	sql = "SELECT * FROM orders WHERE order_id = %s"

	cursor.execute(sql, [id])
	return cursor.fetchone()


def get_amount_for_period(period="daily"):
	"""Returns all the users"""

	db = get_connection()
	if not db: return
	_, cursor = db

	sql = """
		SELECT DATE(`date`) AS order_date, SUM(CAST(`amount` AS DECIMAL(10, 2))) AS revenue
		FROM `orders`
		GROUP BY order_date
		ORDER BY order_date;
	"""
	if period == "monthly": sql = """
		SELECT DATE_FORMAT(`date`, '%Y-%m') AS order_month, SUM(CAST(`amount` AS DECIMAL(10, 2))) AS revenue
		FROM `orders`
		GROUP BY order_month
		ORDER BY order_month;
	"""

	cursor.execute(sql)
	return cursor.fetchall()