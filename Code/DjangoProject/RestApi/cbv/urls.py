from django.conf.urls import url

from cbv import views

urlpatterns =[
    url(r'^book/', views.BookCBV.as_view(), name='book'),
]