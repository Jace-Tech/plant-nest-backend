from functools import wraps

def response(msg: str, data=None, success=True):
  return { "message": msg, "data": data, "success": success }

def get_object(obj):
  new_data = {}
  for key, val in obj.items():
    new_data[key] = str(val)
  return new_data

def get_object_list(seq):
  return [get_object(data) for data in seq]






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

def insert_item(product, cursor ,tableName):
    try:
        user_id = product.get('user_id')
        product_id = product.get('product_id')
        quantity = product.get('quantity')

      
        select_query = F"SELECT * FROM {tableName} WHERE user_id = %s AND product_id = %s"
        cursor.execute(select_query, (user_id, product_id))
        existing_item = cursor.fetchone()

        if existing_item:
           
            new_quantity = existing_item[3] + quantity
            update_query = f"UPDATE {tableName} SET quantity = %s WHERE user_id = %s AND product_id = %s"
            cursor.execute(update_query, (new_quantity, user_id, product_id))
        else:
           
            insert_query = f"INSERT INTO {tableName} (user_id, product_id, quantity) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (user_id, product_id, quantity))

        return True
    except Exception as e:
        raise e
        return False

def remove_product(product, cursor,tableName):
    try:
        delete_query = f"DELETE FROM {tableName} WHERE user_id = %s AND product_id = %s"
        cursor.execute(delete_query, (product.get('user_id'), product.get('product_id')))

        return True
    except Exception as e:
        raise e
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
        raise e
        return None


#review functions 

def insert_review(review, cursor):
    try:  
        insert_query = "INSERT INTO reviews (user_id, product_id, rating, feedback) VALUES (%s, %s, %s, %s)"
        values = (review['user_id'], review['product_id'], review['rating'], review['feedback'])
        cursor.execute(insert_query, values)

        return True  
    except Exception as e:
        return str(e)
