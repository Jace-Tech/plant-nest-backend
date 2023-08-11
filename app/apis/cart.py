from flask import Blueprint, request, jsonify
from ..utils.helpers import select_product, response, select_product, insert_item, remove_product, products_by_user
from ..database import get_connection

cart = Blueprint("cart", __name__)

connection, cursor = get_connection()

tableName = "cart_items"


@cart.get('/add')
def add_to_cart(cursor):
    product =  request.get_json()
    status = insert_item(product,cursor,tableName); 
    
    if status == True:
        return response('Item added to the cart successfully.')
    return response('Item was not added to the cart successfully.', success=False)
    
    
@cart.get('/<user_id>')
def get_cart_contents(user_id):
    
    try:
        user_cart = products_by_user(user_id, cursor,tableName)

        if user_cart is not None:
            cart_with_product_data = []

            for item in user_cart:
                product_id = item['product_id']

                if product_details:
                    item['product_details'] = product_details
                    cart_with_product_data.append(item)

            return response(f'user_id: {user_id}', cart_with_product_data)
        else:
            return response('User not found or cart is empty.', success=False)
    except Exception as e:
        return response('An error occurred.', success=False)


@cart.get('/remove')
def remove_from_cart():
    product =  request.get_json()
    status = remove_product(product,cursor,tableName)
    if status == True:
            return response(f"Item removed from the cart successfully")
    else:
            return response('Product not found in the user\'s cart.',status,success=False), 404
   
