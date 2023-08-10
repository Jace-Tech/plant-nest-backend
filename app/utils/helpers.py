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




#Cart Functions

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


#review functions 

def insert_review(review, cursor):
    try:  
        insert_query = "INSERT INTO reviews (user_id, product_id, rating, feedback) VALUES (%s, %s, %s, %s)"
        values = (review['user_id'], review['product_id'], review['rating'], review['feedback'])
        cursor.execute(insert_query, values)

        return True  
    except Exception as e:
        return str(e)
