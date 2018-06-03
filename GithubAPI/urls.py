from django.conf.urls import url,include
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'', include('RestAPI.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)