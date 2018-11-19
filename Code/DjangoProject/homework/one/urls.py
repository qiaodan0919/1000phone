from django.conf.urls import url

from one import views

urlpatterns =[
    url(r'^hello/', views.hello, name='hello'),
    url(r'^home/', views.home, name='home'),
    url(r'^login/', views.login, name='login'),
    url(r'^register/', views.register, name='register'),
    url(r'^homelogined/', views.home_logined, name='home_logined'),
    url(r'^savemovies/', views.save_movies, name='save_movies'),
    url(r'^saveswipers/', views.save_swipers, name='save_swipers')
]