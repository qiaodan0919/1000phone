from django.conf.urls import url

from mainpage import views

urlpatterns = [
    url(r'^hello', views.hello, name='hello')
]