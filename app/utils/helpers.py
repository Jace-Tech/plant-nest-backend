from functools import wraps
from random import randint

def response(msg: str, data=None, success=True):
	return { "message": msg, "data": data, "success": success }


def generate_id(prefix: str = "id_", length=8):
	id = ""
	for i in range(length):
		id += str(randint(0, 9))
	return prefix + id




