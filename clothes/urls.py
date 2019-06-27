from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from . import views
from hackathon.settings import MEDIA_ROOT
import django

urlpatterns = [
    url(r'^$', views.home, name = 'home'),
    url(r'^toukou/$', views.toukou, name = 'toukou'),
    # url(r'^search/$', views.search, name = 'search'),
    # url(r'media/(?P<path>.*)$', include('django.views.static.serve'), {'document_root': MEDIA_ROOT}),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
