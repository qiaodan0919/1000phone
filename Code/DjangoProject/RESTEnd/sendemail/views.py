from django.http import HttpResponse
from django.shortcuts import render
from .tasks import send_email
# Create your views here.

def mail(request):
    mail_address = request.GET.get('address')

    send_result = send_email.delay(mail_address)

    return HttpResponse(send_result)