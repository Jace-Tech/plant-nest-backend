from flask import request, jsonify
from utils.helpers import select_product 
from app import app

from ..database import get_connection

def create_plant_table():
  db = get_connection()

  if not db: return

  connection, cursor = db


cart_data = {}



@app.route('/api/cart/add/<user_id>/<product_id>/<int:quantity>', methods=['POST'])
def add_to_cart(product,cursor):
    user_id = product['user_id']
    
    if user_id not in cart_data:
        cart_data[user_id] = []
        
    
    productDictionary = select_product(product['product_id'],cursor)
    
    productDictionary['quantity'] = product['quantity']
    
  
    cart_data[user_id].append({"product": productDictionary})
    
    return jsonify({
        'message': 'Item added to the cart successfully.',
        'product':cart_data[user_id]
    })

@app.route('/api/cart/<user_id>', methods=['GET'])
def get_cart_contents(user_id):
    if user_id in cart_data:
        cart_items = cart_data[user_id]
        cart_products = []  
        
        for item in cart_items:
            product = item["product"]
            cart_products.append(product)
        
        return jsonify({'user_id': user_id, 'cart_products': cart_products})
    else:
        return jsonify({'message': 'User not found or cart is empty.'}), 404


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
            return jsonify({
                'message': 'Item removed from the cart successfully.',
                'removed_product': removed_product
            })
        else:
            return jsonify({'message': 'Product not found in the user\'s cart.'}), 404
    else:
        return jsonify({'message': 'User not found or cart is empty.'}), 404

