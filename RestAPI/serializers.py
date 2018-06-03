# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from rest_framework import serializers
from RestAPI.models import *

class ActorSerializers(serializers.ModelSerializer):
	id = serializers.SerializerMethodField('get_obj_id')

	class Meta:
		model = Actor
		fields = ('id','avatar_url','login')

	def get_obj_id(self,obj):
		return obj.base_id

class RepoSerializers(serializers.ModelSerializer):
	id = serializers.SerializerMethodField('get_obj_id')

	class Meta:
		model = Repo
		fields = ('id','name','url')

	def get_obj_id(self,obj):
		return obj.base_id

class EventSerializers(serializers.ModelSerializer):
	actor = ActorSerializers()
	repo = RepoSerializers()
	created_at = serializers.ReadOnlyField(source='get_str_date')
	type = serializers.ReadOnlyField(source='get_event_type')
	id = serializers.ReadOnlyField(source='get_obj_id')

	class Meta:
		model = Events
		fields = ('type','id','actor', 'repo','created_at')

	
	# def get_str_date(self,obj):
	# 	return datetime.datetime.strftime(obj.created_at,'%Y-%m-%d %H:%M:%S')

	# def get_event_type(self,obj):
	# 	return obj.created_at

	# def get_obj_id(self,obj):

	# 	return obj.base_id





