# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import datetime


class BaseId(models.Model):
	base_id = models.IntegerField(blank=False,primary_key=True)
	
	class Meta:
		abstract = True
		
		
class ImageCollection(BaseId):
	image_url = models.CharField(max_length=1000)
	content_model = models.CharField(max_length=50)
	
	
	def __unicode__(self):
		return self.image_url

class Actor(BaseId):
	avatar_url = models.CharField(max_length=1000)
	login = models.CharField(max_length=100,unique=True)
	event_count = models.IntegerField(default=0)
	latest_event_date = models.DateTimeField(blank=False)
	
	def __unicode__(self):
		return self.login

	def save_image(self,image_url):
		img_obj = ImageCollection(image_url = image_url,content_model=self.__class__.__name__)
		img_obj.save()
		return img_obj



class Repo(BaseId):
	name = models.CharField(max_length=100)
	url = models.URLField(max_length=1000)
	
	def __unicode__(self):
		return self.name

class Events(BaseId):
	event_type = models.CharField(max_length=50)
	created_at = models.DateTimeField(blank=False)
	actor = models.ForeignKey(Actor)
	repo = models.ForeignKey(Repo)
	
	def dateFormat(self):
		return '%Y-%m-%d %H:%M:%S'
	
	def __unicode__(self):
		return self.event_type
	
	def save(self,*args,**kwargs):
		try:
			valid_date = datetime.datetime.strftime(self.created_at,self.dateFormat())
		except ValueError:
			valid_date = False
		if not valid_date:
			return False
		else:
			super(Events,self).save(*args,**kwargs)

	def get_str_date(self):
		return unicode(datetime.datetime.strftime(self.created_at,'%Y-%m-%d %H:%M:%S'),'utf-8')

	def get_event_type(self):
		return self.event_type

	def get_obj_id(self):

		return self.base_id




	