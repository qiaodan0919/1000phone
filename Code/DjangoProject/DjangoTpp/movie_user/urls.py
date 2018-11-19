from django.conf.urls import url

from movie_user import views

urlpatterns = [
    url(r'^movieusers/', views.MovieUsersApi.as_view()),
    url(r'^movieorders/$', views.MovieOrdersApi.as_view()),
    url(r'^movieorders/(?P<typeid>\d+)/$', views.MovieOrderApi.as_view())
]