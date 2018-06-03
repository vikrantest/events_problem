from django.conf.urls import url,include
from rest_framework.urlpatterns import format_suffix_patterns
from RestAPI.views import EventView,ActorView
from RestAPI.filterviews import ActorEvents,ActorStreak


urlpatterns = [
    url(r'^events/$', EventView.as_view()),
    url(r'^erase/$', EventView.as_view()),
    url(r'^actors/$', ActorView.as_view()),
    url(r'^actors/streak/$', ActorStreak.as_view()),
    url(r'^events/actors/(?P<actor_id>[0-9]+)/$', ActorEvents.as_view()),
]