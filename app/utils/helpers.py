from functools import wraps
from random import randint

def response(msg: str, data=None, success=True):
	return { "message": msg, "data": data, "success": success }


def generate_id(prefix: str = "id_", length=8):
	id = ""
	for i in range(length):
		id += str(randint(0, 9))
	return prefix + id


def map_func(seq, func):
	"Emulates Javascript's map array method"
	res = []
	for index, item in enumerate(seq):
		res.append(func(item, index, seq))
	return res


def filter_func(seq, func):
	"Emulates Javascript's filter array method"
	res = []
	for index, item in enumerate(seq):
		if func(item, index, seq):
			res.append(item)
	return res


def dict_except(obj, *unused):
	new_obj = {**obj}
	for key in obj:
		if key in unused: del new_obj[key]
	return new_obj
		