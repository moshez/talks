from django.conf.urls import url

from twemo.simple import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
