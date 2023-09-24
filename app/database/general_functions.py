from datetime import datetime
def select_product(product_id,cursor):
	try:
		# Prepare and execute the SQL query
		query = "SELECT * FROM plants WHERE plant_id = %s"
		cursor.execute(query, (product_id,))

		# Fetch the result
		product = cursor.fetchone()

		if product:
			return str(product)
		else:
			return "Plant not found."
	except Exception as e:
		return str(e)


def insert_item(product, db, tableName):
    conn, cursor = db
    try:
        user_id = product.get('user_id')
        product_id = product.get('product_id')
        quantity = product.get('quantity')

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_query = f"INSERT INTO {tableName} (user_id, product_id, quantity, date) VALUES (%s, %s, %s, %s)"
        
        # Execute the insert query and commit changes
        cursor.execute(insert_query, (user_id, product_id,quantity, now))
        conn.commit()
        
        return True
    except Exception as e:
        print("INSERT ERROR:", str(e))
        # Rollback changes if an error occurred
        conn.rollback()
        
    return False



def remove_product(product, db,tableName):
	connection, cursor = db
	try:
		delete_query = f"DELETE FROM {tableName} WHERE user_id = %s AND product_id = %s"
		cursor.execute(delete_query, (product.get('user_id'), product.get('product_id')))
		connection.commit()

		return True
	except Exception as e:
		print("REMOVE ERROR:", str(e))
		
	return False


def products_by_user(user_id, cursor,tableName):
	try:
		select_query = f"SELECT * FROM {tableName} WHERE user_id = %s"
		cursor.execute(select_query, (user_id,))
		product_items = cursor.fetchall()

		# Prepare a list to hold the selected products
		selected_products = []

		for product_item in product_items:
			user_id = product_item[1]
			product_id = product_item[2]
			quantity = product_item[3]
			selected_products.append({
				'user_id': user_id,
				'product_id': product_id,
				'quantity': quantity
			})

		return selected_products
	except Exception as e:
		print("PRODUCTS ERROR:", str(e))
		
	return None


def insert_review(review, db):
	connection, cursor = db
	try:
		now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		insert_query = "INSERT INTO reviews (user_id, product_id, rating, feedback, date) VALUES (%s, %s, %s, %s, %s)"
		values = (review['user_id'], review['product_id'], review['rating'], review['feedback'], now)
		cursor.execute(insert_query, values)
		connection.commit()

		return True

	except Exception as e:
		return str(e)

def fetch_product_review(product_id, cursor):
	try:
		query = "SELECT AVG(rating) AS average_rating FROM reviews WHERE product_id = %s"
		cursor.execute(query, (product_id,))


		result = cursor.fetchone()

		if result and result['average_rating'] is not None:
			return result['average_rating']
		else:
			return "Product not found or no reviews available."

	except Exception as e:
		return str(e)
