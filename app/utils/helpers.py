from functools import wraps
from datetime import datetime

def response(msg: str, data=None, success=True):
	return { "message": msg, "data": data, "success": success }


def generate_id(prefix: str = "id_"):
	timestamp = datetime.now().timestamp()
	return prefix + str(timestamp)




