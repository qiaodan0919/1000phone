import json

from django.http import JsonResponse, QueryDict
from django.shortcuts import render

# Create your views here.
from django.views import View

from cbv.models import Book


class BookCBV(View):

    def get(self, requset):

        book_list = Book.objects.all()
        book_list_json = []

        for book in book_list:
            book_list_json.append(book.to_dict())

        data = {
            'status': 200,
            'msg': 'ok',
            'data': book_list_json,
        }

        return JsonResponse(data=data)

    def post(self, request):

        b_name = request.POST.get('b_name')
        b_price = request.POST.get('b_price')

        book = Book()
        book.b_name = b_name
        book.b_price = b_price
        book.save()

        data = {
            'status': 200,
            'msg': 'ok',
            'data': book.to_dict(),
        }
        return JsonResponse(data=data)

    def put(self, request):
        put = QueryDict(request.body.decode("utf-8"), encoding=request.encoding)
        print(put)
        b_name = put.get('b_name')
        b_price = put.get('b_price')
        print(b_name,b_price)

        return JsonResponse({'msg': 'ok'})

    def delete(self, request):
        b_name = request.DELETE.get('b_name')
        print(b_name)
        book = Book.objects.get(b_name=b_name)
        book_msg = book.to_dict()
        book.delete()
        data = {
            'status': 200,
            'msg': 'ok',
            'data': book_msg,
        }
        return JsonResponse(data=data)
