from flask import Blueprint, request, jsonify
from ..utils.helpers import response
from ..database.general_functions import insert_review,fetch_product_review

from ..database import get_connection

review = Blueprint("review", __name__)

db = get_connection()
connection, cursor = db



@review.post('/review')
def submit_review():
    review = request.json
    status = insert_review(review,db)
    if status:
        return response('Feedback submitted successfully.')
    else:
        return response("feedback not submitted", success=False)


@review.get('/average_ratings/<product_id>')
def average_rating(product_id):
    status = fetch_product_review(product_id,cursor)
    if status is not None :
        return response('successfull',status)
    return response('No reviews available for this product.')
    
    


