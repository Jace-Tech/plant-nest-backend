from . import get_connection
from database.general_functions import select_product

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

def get_all_reviews():
    """Returns all the reviews"""

    db = get_connection()
    if not db: return
    _, cursor = db
    sql = "SELECT * FROM reviews"

    cursor.execute(sql)
    return cursor.fetchall()

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
        if not db: return
        _, cursor = db
        
        products_query = "SELECT product_id, product_name FROM products"
        cursor.execute(products_query)
        products = cursor.fetchall()
        
        products_with_ratings = []
        
        for product in products:
            product_id = product['product_id']
            product_details = select_product(product_id, cursor)
            
            if product_details:
                average_rating = calculate_average_rating(product_id, cursor)
                
                products_with_ratings.append({
                    'product_id': product_id,
                    'product_name': product['product_name'],
                    'average_rating': average_rating,
                    'product_details': product_details
                })
        
        return products_with_ratings
    
    except Exception as e:
        return False
    
    finally:
        if db:
            db.close()
