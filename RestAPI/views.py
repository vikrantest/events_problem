# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from RestAPI.validators import Validators
from RestAPI.models import *
from RestAPI.serializers import *



class EventView(APIView):

	def validateRequest(self,data):
		return Validators.mainValidator(data)


	
	def actorGetSetObject(self,data,latest_event_date):
		actor_data = Actor.objects.filter(login=data.get('login'))
		if actor_data:
			actor_data = actor_data[0]
		else:
			actor_data = Actor(login=data.get('login'),base_id=data.get('id'))
			actor_data.avatar_url = data.get('avatar_url')
		actor_data.latest_event_date = latest_event_date
		actor_data.event_count+=1
		actor_data.save()
		return actor_data

	def repoGetSetObject(self,data):
		repo_data = Repo.objects.filter(base_id=data.get('id'))
		if repo_data:
			return repo_data[0]
		else:
			repo_data = Repo.objects.create(base_id=data.get('id'),name=data.get('name'),url=data.get('url'))
			return repo_data

	
	def post(self,request):
		try:
			request_data = self.request.data
			if self.validateRequest(request_data):
				created_at = datetime.datetime.strptime(request_data.get('created_at'),Validators.DATE_FORMAT)
				actor=self.actorGetSetObject(request_data.get('actor'),created_at)
				repo=self.repoGetSetObject(request_data.get('repo'))
				events = Events.objects.create(base_id = request_data.get('id'),created_at=created_at,repo=repo,actor=actor,event_type=request_data.get('type'))
				
				return Response({},status=status.HTTP_201_CREATED)
			else:
				return Response({},status=status.HTTP_400_BAD_REQUEST)
		except:
			print sys.exc_info()


	def get(self,request):

		events_data = Events.objects.order_by('base_id')

		serialized_events_data = EventSerializers(events_data,many=True).data

		return Response(serialized_events_data,status=status.HTTP_200_OK)

	def delete(self,request):
		Events.objects.all().delete()
		return Response({"body": {}, "headers": {}},status=status.HTTP_200_OK)

class ActorView(APIView):

	def validateRequest(self,data):
		return data.get('avatar_url')

	def get(self,request):
		actors = Actor.objects.order_by('-event_count','-latest_event_date','login')
		# for m in actors:print m.event_count,m.login,m.latest_event_date
		actors_list = ActorSerializers(actors,many=True).data
		return Response(actors_list,status=status.HTTP_200_OK)


	def put(self,request):
		request_data = self.request.data
		if not self.validateRequest(request_data):
			return Response({},status=status.HTTP_400_BAD_REQUEST)
		try:
			actor = Actor.objects.get(login = request_data.get('login'))
			actor.avatar_url = request_data.get('avatar_url')
			actor.save()
			return Response({},status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			return Response({},status=status.HTTP_404_NOT_FOUND)



	