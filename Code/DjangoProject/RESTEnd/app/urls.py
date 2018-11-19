from django.conf.urls import url

from app import views

urlpatterns = [
    url(r'^users/$', views.UsersView.as_view()),
    url(r'^users/(?P<pk>\d+)/$', views.UserView.as_view(), name='usermodel-detail'),
    url(r'^address/$', views.AddressView.as_view({
        'post': 'create',
        'get': 'list',
    })),
    url(r'^users/(?P<pk>\d+)/$', views.AddressView.as_view({
        'get': 'retrieve',
    }), name='addressmodel-detail'),

]