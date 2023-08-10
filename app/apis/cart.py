from flask import Blueprint, request, jsonify
from utils.helpers import select_product,response 
from app import app

from ..database import get_connection

cart = Blueprint("cart", __name__)

connection, cursor = get_connection()


cart_data = {}



@app.route('/api/cart/add/<user_id>/<product_id>/<int:quantity>', methods=['POST'])
def add_to_cart(product,cursor):
    user_id = product['user_id']
    
    if user_id not in cart_data:
        cart_data[user_id] = []
        
    
    productDictionary = select_product(product['product_id'],cursor)
    
    productDictionary['quantity'] = product['quantity']
    
  
    cart_data[user_id].append({"product": productDictionary})
    
    return response('Item added to the cart successfully.',cart_data[user_id])
    
@app.route('/api/cart/<user_id>', methods=['GET'])
def get_cart_contents(user_id):
    if user_id in cart_data:
        cart_items = cart_data[user_id]
        cart_products = []  
        
        for item in cart_items:
            product = item["product"]
            cart_products.append(product)
        
        return response(f"user_id': {user_id}",cart_products)
    else:
        return response(f"User not found or cart is empty.",success=False)


@app.route('/api/cart/remove/<user_id>/<product_id>', methods=['DELETE'])
def remove_from_cart(user_id, product_id):
    if user_id in cart_data:
        cart_items = cart_data[user_id]
        
      
        index_to_remove = None
        for index, item in enumerate(cart_items):
            if item["product"]["product_id"] == product_id:
                index_to_remove = index
                break
        
        if index_to_remove is not None:
            removed_product = cart_items.pop(index_to_remove)
            return response(f"Item removed from the cart successfully", removed_product)
        else:
            return response('Product not found in the user\'s cart.',success=False), 404
    else:
        return response('User not found or cart is empty.',success=False), 404

