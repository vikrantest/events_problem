import sys
import os
import datetime
from collections import Counter
from RestAPI.utils import *
from RestAPI.models import *
from django.apps import apps


class Validators(object):
	REPO_FILEDS = ['id','name','url']
	ACTOR_FIELDS = ['id','login','avatar_url']
	EVENTS_FIELDS = ['repo','actor','id','created_at','type']
	MANDATORY_VALIDATION = True
	DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


	@classmethod
	def mainValidator(cls,data,fields=[]):
		if cls.MANDATORY_VALIDATION:
			mandatory_validated = cls.mandatoryValidation(data,fields)



		if mandatory_validated:
			try:
				valid_date = datetime.datetime.strptime(data.get('created_at'),cls.DATE_FORMAT)
			except ValueError:
				return False
		else:
			return False


		if Validators.validateID(data.get('id'),'Events'):
			return False
		else:
			return True




	@classmethod
	def mandatoryValidation(cls,data,fields):
		main_keys = data.keys()
		if fields:
			return Counter(main_keys) == Counter(fields)
		else:
			return all([Counter(main_keys) == Counter(cls.EVENTS_FIELDS) , Counter(data.get('repo').keys()) == Counter(cls.REPO_FILEDS) ,  Counter(data.get('actor').keys()) == Counter(cls.ACTOR_FIELDS)])

	@staticmethod
	def validateID(id,model_name):
		model = apps.get_model('RestAPI.'+model_name)
		return model.objects.filter(base_id=id).exists()


	





			