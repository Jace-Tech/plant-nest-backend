from flask import Blueprint, request
from ..utils.helpers import response
from ..database.general_functions import insert_feedback
from ..database import get_connection

feedback = Blueprint("feedback", __name__)


@feedback.post('/')
def submit_review():
    feedback_data = request.json
    status = insert_feedback(feedback_data)
    if status:
         return response('Feedback submitted successfully.',feedback_data)
    else:
        return response("feedback not submitted", success=False)



