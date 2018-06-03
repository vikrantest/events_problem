import sys

def dict_key_search(key, var):
	if isinstance(var,dict):
		for k, v in var.iteritems():
			if k == key:
				return v
			if isinstance(v, dict):
				return dict_key_search(key, v)
			elif isinstance(v, list):
				for x in v:
					return dict_key_search(key, x)
