from . import get_connection


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



def create_reviews_table():
    db = get_connection()
    if not db: return
    connection, cursor = db

    sql = """CREATE TABLE IF NOT EXISTS reviews (
        review_id INT PRIMARY KEY AUTO_INCREMENT,
        user_id VARCHAR(20),
        isDeleted INT NOT NULL,
        product_id VARCHAR(20),
        rating INT NOT NULL,
        feedback TEXT,
        `date` DATETIME
    )"""

    cursor.execute(sql)
    connection.commit()
    print("TABLE CREATED!")
    connection.close()

def get_all_reviews(cursor):
    """Returns all the reviews with corresponding product names"""

    db = get_connection()
    if not db: return
    _, cursor = db
    sql = "SELECT * FROM reviews"

    cursor.execute(sql)
    reviews = cursor.fetchall()

    reviews_with_products = []

    for review in reviews:
        product_id = review['product_id']
        product = select_product(product_id, cursor)
        
        if product:
            review['product_name'] = product['name']
            reviews_with_products.append(review)

    return reviews_with_products

def calculate_average_rating(product_id, cursor):
    try:
        ratings_query = f"SELECT SUM(rating) as total_rating FROM reviews WHERE product_id = %s"
        cursor.execute(ratings_query, (product_id,))
        total_rating = cursor.fetchone()['total_rating']
        
        count_query = f"SELECT COUNT(*) as review_count FROM reviews WHERE product_id = %s"
        cursor.execute(count_query, (product_id,))
        review_count = cursor.fetchone()['review_count']
        
        if total_rating is not None and review_count > 0:
            average_rating = total_rating / review_count
        else:
            average_rating = 0
        
        return average_rating
    except Exception as e:
        return False



def fetch_products_with_average_ratings():
    try:
        db = get_connection()
        if not db:
            return
        
        _, cursor = db
        
        products_query = "SELECT product_id, product_name, price, quantity FROM products"
        cursor.execute(products_query)
        products = cursor.fetchall()
        
        products_with_ratings = []
        
        for product in products:
            product_id = product['product_id']
            product_details = select_product(product_id, cursor)
            
            if product_details:
                average_rating = calculate_average_rating(product_id, cursor)
                
                products_with_ratings.append({
                    'product_name': product_details.get('name'),
                    'price': product['price'],
                    'quantity': product['quantity'],
                    'average_rating': average_rating
                })
        
        return products_with_ratings
    
    except Exception as e:
        return False
    
    finally:
        if db:
            db.close()