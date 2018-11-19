from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from RESTApi import views

urlpatterns = [
    url(r'^users/$', views.UsersView.as_view()),
    url(r'^users/(?P<pk>\d+)/$', views.UserView.as_view(), name='usermodel-detail'),
]

# router = DefaultRouter()
#
# router.register(r'users', UserModelViewSet)