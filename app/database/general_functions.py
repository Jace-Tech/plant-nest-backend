from . import get_connection
from datetime import datetime

def select_product(product_id):
    db = get_connection()
    if not db:
        return
    _, cursor = db
    try:
        query = "SELECT * FROM plants WHERE plant_id = %s"
        cursor.execute(query, (product_id,))
        product = cursor.fetchone()

        if product:
            return str(product)
        else:
            return "Plant not found."
    except Exception as e:
        return str(e)

def insert_item(product,table_name):
    db = get_connection()
    if not db:
        return
    conn, cursor = db
    try:
        user_id = product.get('user_id')
        product_id = product.get('product_id')
        quantity = product.get('quantity')

        select_query = f"SELECT * FROM {table_name} WHERE user_id = %s AND product_id = %s"
        cursor.execute(select_query, (user_id, product_id))
        existing_item = cursor.fetchone()

        if existing_item:
            new_quantity = existing_item[3] + quantity
            update_query = f"UPDATE {table_name} SET quantity = %s WHERE user_id = %s AND product_id = %s"
            cursor.execute(update_query, (new_quantity, user_id, product_id))
        else:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            insert_query = f"INSERT INTO {table_name} (user_id, product_id, quantity, date) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (user_id, product_id, quantity, now))

        conn.commit()

        return True
    except Exception as e:
        print("INSERT ERROR:", str(e))
        return False

def remove_product(product, table_name):
    db = get_connection()
    if not db:
        return
    conn, cursor = db
    try:
        delete_query = f"DELETE FROM {table_name} WHERE user_id = %s AND product_id = %s"
        cursor.execute(delete_query, (product.get('user_id'), product.get('product_id')))
        conn.commit()

        return True
    except Exception as e:
        print("REMOVE ERROR:", str(e))
        return False

def products_by_user(user_id, table_name):
    db = get_connection()
    if not db:
        return
    _, cursor = db
    try:
        select_query = f"SELECT * FROM {table_name} WHERE user_id = %s"
        cursor.execute(select_query, (user_id,))
        product_items = cursor.fetchall()
        print(product_items)

        selected_products = []

        for product_item in product_items:
            user_id = product_item['user_id']
            product_id = product_item['product_id']
            quantity = product_item['quantity']
            selected_products.append({
                'user_id': user_id,
                'product_id': product_id,
                'quantity': quantity
            })
            print(product_item)

        return selected_products
    except Exception as e:
        print("PRODUCTS ERROR:", str(e))
        return None

def insert_review(review):
    db = get_connection()
    if not db:
        return
    conn, cursor = db
    try:
        user_id = review.get('user_id')
        product_id = review.get('product_id')
        rating = review.get('rating')
        feedback = review.get('feedback')
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_query = "INSERT INTO reviews (user_id, product_id, rating, feedback, date) VALUES (%s, %s, %s, %s, %s)"
        values = (user_id, product_id, rating, feedback, now)
        cursor.execute(insert_query, values)
        conn.commit()
        return True
    except Exception as e:
        print (str(e))
        return str(e)

def fetch_product_review(product_id):
    db = get_connection()
    if not db:
        return
    _, cursor = db
    try:
        query = "SELECT AVG(rating) AS average_rating FROM reviews WHERE product_id = %s"
        cursor.execute(query, (product_id,))
        result = cursor.fetchone()
        print(result)

        if result and result['average_rating'] is not None:
            return result['average_rating']
        else:
            return "Product not found or no reviews available."
    except Exception as e:
        return str(e)



def insert_feedback(feedbacks):
    db = get_connection()
    if not db:
        return
    conn, cursor = db
    try:
        name = feedbacks.get('name')
        email = feedbacks.get('email')
        message = feedbacks.get('message')
       
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_query = "INSERT INTO feedback (name, email, message, date) VALUES (%s, %s, %s, %s, %s)"
        values = (name, email, message, now)
        cursor.execute(insert_query, values)
        conn.commit()
        return True
    except Exception as e:
        print (str(e))
        return str(e)



