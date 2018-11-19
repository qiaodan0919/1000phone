from django.conf.urls import url

from RESTTwo import views

urlpatterns =[
    url(r'^students', views.StudentsView.as_view(), name='stusent'),
    url(r'^students/(?P<bookid>\d+)', views.StudentView.as_view(), name='stusent'),

]