from flask import Blueprint, request, jsonify
from ..utils.helpers import response
from ..database.general_functions import insert_review,fetch_product_review

from ..database import get_connection

review = Blueprint("review", __name__)

connection, cursor = get_connection()


@review.post('/review')
def submit_feedback():
    review = request.json('review')
    status = insert_review(review,cursor)
    if status:
         return response('Feedback submitted successfully.')
    else:
        return response("feedback not submitted", success=False)


@review.get('/average_ratings/<int:product_id>')

def average_rating(product_id):
    status = fetch_product_review(product_id,cursor)
    if status is not None :
        return response('successfull',status)
    return response('No reviews available for this product.')
    
    


