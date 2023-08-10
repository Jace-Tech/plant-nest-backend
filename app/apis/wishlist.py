from flask import request, jsonify
from utils.helpers import select_product 
from app import app

from ..database import get_connection

def create_plant_table():
  db = get_connection()

  if not db: return

  connection, cursor = db


wishlist_data = {}




@app.route('/api/wishlist/add/<user_id>/<product_id>', methods=['POST'])
def add_to_wishlist(user_id, product_id):
    if user_id not in wishlist_data:
        wishlist_data[user_id] = []

 
    product = select_product(product_id)

    
    if product not in wishlist_data[user_id]:
        wishlist_data[user_id].append(product)
        return jsonify({
            'message': 'Product added to wishlist successfully.',
            'product': product
        })
    else:
        return jsonify({
            'message': 'Product is already in the wishlist.',
            'product': product
        })

@app.route('/api/wishlist/<user_id>', methods=['GET'])
def get_wishlist_contents(user_id):
    if user_id in wishlist_data:
        wishlist_products = wishlist_data[user_id]
        return jsonify({'user_id': user_id, 'wishlist_products': wishlist_products})
    else:
        return jsonify({'message': 'User not found or wishlist is empty.'}), 404

@app.route('/api/wishlist/remove/<user_id>/<product_id>', methods=['DELETE'])
def remove_from_wishlist(user_id, product_id):
    if user_id in wishlist_data:
        wishlist_products = wishlist_data[user_id]

      
        product_to_remove = None
        for product in wishlist_products:
            if product["product_id"] == product_id:
                product_to_remove = product
                break
        
        if product_to_remove:
            wishlist_products.remove(product_to_remove)
            return jsonify({
                'message': 'Product removed from wishlist successfully.',
                'removed_product': product_to_remove
            })
        else:
            return jsonify({'message': 'Product not found in the user\'s wishlist.'}), 404
    else:
        return jsonify({'message': 'User not found or wishlist is empty.'}), 404
