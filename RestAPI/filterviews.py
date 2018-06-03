# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from collections import *
import operator
from RestAPI.validators import Validators
from RestAPI.models import *
from RestAPI.serializers import *




class ActorEvents(APIView):

    def get(self,request,actor_id):
        if actor_id:
            try:
                events = Events.objects.filter(actor__base_id = actor_id).order_by('-base_id')
                events_data = EventSerializers(events,many=True).data
                return Response(events_data,status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({},status=status.HTTP_400_BAD_REQUEST)


class ActorStreak(APIView):

    def get(self,request):
        streak_result = {}
        final_result = []
        cons_count = 1
        last_date = ''
        queryset =  Events.objects.order_by('-created_at')
        # main_queryset = queryset.extra(select = {'id':'actor__base_id','login':'actor__login','avatar_url':'actor__avatar_url'}).values('id','login','created_at','avatar_url')
        main_queryset = queryset.values('actor__base_id','actor__login','created_at','actor__avatar_url')
        for m in main_queryset:
            print m['actor__login']
        print '+++++++++++++++++++',len(main_queryset)
        print main_queryset[len(main_queryset)-2:]

        for m in xrange(0,len(main_queryset)):
            print m,len(main_queryset)-1,cons_count
            if m == len(main_queryset)-1 and cons_count == 1:
                print '+++++wo+++++++'
                try:
                    new_obj = {'id':main_queryset[m]['actor__base_id'],'login':main_queryset[m]['actor__login'],'avatar_url':main_queryset[m]['actor__avatar_url'],'created_at':main_queryset[m]['created_at']}
                    if streak_result.get(cons_count):
                        streak_result[cons_count].append(new_obj)
                    else:
                        streak_result[cons_count] = [new_obj]
                except:
                    import sys
                    print sys.exc_info()
            else:
                print '+++++++++++++',m
                if main_queryset[m]['actor__login'] == main_queryset[m+1]['actor__login']:
                    cons_count+=1
                    if cons_count == 2:
                        last_date = main_queryset[m]['created_at']
                else:
                    if cons_count>1:
                        main_queryset[m]['created_at'] = last_date
                    last_date = ''
                    new_obj = {'id':main_queryset[m]['actor__base_id'],'login':main_queryset[m]['actor__login'],'avatar_url':main_queryset[m]['actor__avatar_url'],'created_at':main_queryset[m]['created_at']}
                    if streak_result.get(cons_count):
                        streak_result[cons_count].append(new_obj)
                    else:
                        streak_result[cons_count] = [new_obj]
                    cons_count = 1
        # if main_queryset[]
        streak_result = OrderedDict(sorted(streak_result.items(), reverse=True))
        for m in streak_result[1]:
            print m['login']
        print '+++++++++++============='
        for k,v in streak_result.items():
            v = sorted(v, key=operator.itemgetter('created_at', 'login'),reverse=True)
            map(lambda x: x.pop('created_at'),v)
            final_result.extend(v)
            # for i in v:
            #   print k,i


        return Response(final_result,status=status.HTTP_200_OK)


