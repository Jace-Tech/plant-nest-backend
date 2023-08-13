from flask import Blueprint, request, jsonify
from ..utils.helpers import response

from ..database import get_connection
from ..database.general_functions import select_product,select_product,insert_item,remove_product,products_by_user

cart = Blueprint("cart", __name__)

db = get_connection()
connection, cursor = db


tableName = "cart_items"


@cart.post('/add')
def add_to_cart():
    product =  request.json
    
    status = insert_item(product,tableName); 
    
    
    if status == True:
        return response('Item added to the cart successfully.',product)
    
    return response('Item was not added to the cart successfully.', success=False)
    
    
@cart.get('/<user_id>')
def get_cart_contents(user_id):
    
    print(user_id)
    
    try:
        user_cart = products_by_user(user_id,tableName)
        
              
        
        print(user_cart)
        if user_cart is not None:
            cart_with_product_data = []

            for item in user_cart:
                product_id = item['product_id']
                product_details = select_product(product_id)

                if product_details:
                    item['product_details'] = product_details
                    cart_with_product_data.append(item)

            return response(f'request successfull', cart_with_product_data)
        else:
            return response('User not  found or cart is empty.', success=False)
    except Exception as e:
        return response('An error occurred.', success=False)


@cart.post('/remove')
def remove_from_cart():
    product =  request.json
    status = remove_product(product,tableName)
    if status == True:
        return response(f"Item removed from the cart successfully")
    else:
        return response('Product not found in the user\'s cart.',status,success=False), 404
