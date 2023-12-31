from flask import Blueprint, request, jsonify
from ..utils.helpers import response
from ..database.general_functions import select_product,select_product,insert_item,remove_product,products_by_user
from ..database import get_connection

wishlist = Blueprint("wishlist", __name__)
db = get_connection()
connection, cursor = db
tableName = "wishlist_items"


@wishlist.post('/add')
def add_to_wishlist():
    product =  request.json
    
    status = insert_item(product,db,tableName); 
    
    if status == True:
        return response('Item added to the wishlist successfully.')
    
    return response('Item was not added to the wishlist successfully.', success=False)
    
    
@wishlist.get('/<user_id>')
def get_wishlist_contents(user_id):
    
    try:
        user_wishlist = products_by_user(user_id, cursor,tableName)

        if user_wishlist is not None:
            wishlist_with_product_data = []

            for item in user_wishlist:
                product_id = item['product_id']
                product_details = select_product(product_id, cursor)
                if product_details:
                    item['product_details'] = product_details
                    wishlist_with_product_data.append(item)

            return response(f'user_id: {user_id}', wishlist_with_product_data)
        else:
            return response('User not found or wishlist is empty.', success=False)
    except Exception as e:
        return response('An error occurred.', success=False)


@wishlist.post('/remove')
def remove_from_wishlist():
    product =  request.json
    status = remove_product(product,db,tableName)
    if status == True:
        return response(f"Item removed from the wishlist successfully")
    else:
        return response('Product not found in the user\'s wishlist.',status,success=False), 404
   

