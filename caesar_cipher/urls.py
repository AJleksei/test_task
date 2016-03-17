"""
from django.conf.urls import url
from django.contrib import admin
import views


urlpatterns = [
    url(r'^test/$', views.test, name='test'),
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),

]
"""