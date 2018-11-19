from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from RESTTwo.models import Students
from RESTTwo.serializers import StudentsSerializer


class StudentsView(APIView):

    def post(self, request):
        # s_name = request.POST.get('s_name')
        #
        # s_age = request.POST.get('s_age')
        #
        # student = Students()
        # student.s_name = s_name
        # student.s_age = s_age
        # student.save()
        #
        # student_serializer = StudentsSerializer(student)
        # print('---------')
        data = JSONParser().parse(request)
        print(data)
        student_serializer = StudentsSerializer(data=data)
        if student_serializer.is_valid():
            student_serializer.save()
            return JsonResponse(student_serializer.data)
        return JsonResponse(student_serializer.errors)

    def get(self,request):
        students = Students.objects.all()
        students_serializer = StudentsSerializer(students, many=True)
        data = {
            'status': 200,
            'students': students_serializer.data
        }
        return JsonResponse(data=data)

    def put(self,request):

        print(request.data)

        return JsonResponse({'msg':'ok'})

    def delete(self, request):

        return  JsonResponse({'msg': 'delete'})


class StudentView(APIView):
    def get(self,request):
        pass

    def delete(self,request):
        pass


    def put(self, request):
        pass
