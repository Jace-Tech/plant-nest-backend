from flask import Blueprint, request, jsonify
from utils.helpers import select_product,response
from app import app

from ..database import get_connection

wishlist = Blueprint("wishlist", __name__)

connection, cursor = get_connection()


wishlist_data = {}




@app.route('/api/wishlist/add/<product_id>', methods=['POST'])
def add_to_wishlist(wishlist):
    
    user_id = wishlist['user_id']
    
    if user_id not in wishlist_data:
        wishlist_data[user_id] = []

    product = select_product(wishlist['product_id'])

    if product:
        try:
            if product not in wishlist_data[user_id]:
                wishlist_data[user_id].append(product)
                return response(
                    'Product added to wishlist successfully.',
                    product
                )
            else:
                return response('Product is already in the wishlist.', product, success=False)
        except Exception as e:
            return response('Error adding product to wishlist.', error=str(e), success=False)

    if user_id not in wishlist_data:
        wishlist_data[user_id] = []

 
    product = select_product(wishlist['product_id'])

    
    if product not in wishlist_data[user_id]:
        wishlist_data[user_id].append(product)
        return response(
            'Product added to wishlist successfully.',
            product
        )
    else:
        return response('Product is already in the wishlist.', product ,success=False )

@app.route('/api/wishlist/<user_id>', methods=['GET'])
def get_wishlist_contents(user_id):
    if user_id in wishlist_data:
        wishlist_products = wishlist_data[user_id]
        return response(F'user_id: {user_id} ', wishlist_products)
    else:
        return response('User not found or wishlist is empty.',success=False), 404

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
            return response('Product removed from wishlist successfully.', product_to_remove)
        else:
            return response('Product not found in the user\'s wishlist.',success=False), 404
    else:
        return jsonify({'message': 'User not found or wishlist is empty.'}), 404
