import re

import requests
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
from django.urls import reverse

from one import models
from one.models import User, Movies, Swiper


def hello(request):
    return HttpResponse('Heollo World')


def home(request):
    # username = request.session.get("username")
    # user = User.objects.get(u_name=username)
    # print(username)
    print(request.user.is_authenticated())
    if request.user.is_authenticated():

        return render(request, 'home_logined.html', context=locals())
    else:
        return render(request, 'home.html')


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        passwdone = request.POST.get('passwdone')
        passwdtwo = request.POST.get('passwdtwo')
        email = request.POST.get('email')
        file = request.FILES.get('file')
        print(request.FILES.get('file'))
        print(username)
        if (len(username)>5 and len(username)<11):
            pass
        else:
            return HttpResponse('用户名错误，请重新注册')

        if re.match("^(?:(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])).{5,10}$",passwdone):
            pass
        else:
            return HttpResponse('密码格式错误，请重新注册')

        if passwdone==passwdtwo:
            pass
        else:
            return HttpResponse('两次密码不一致，请重新注册')

        if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email):
            user = User()
            user.u_name = username
            user.u_passwd = passwdone
            user.u_email = email
            user.u_file = file
            user.save()
            return redirect(reverse('one:login'))
        else:
            return HttpResponse('邮箱格式错误，请重新注册')




def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get("username")
        passwd = request.POST.get("passwd")
        user = models.User.objects.filter(u_name=username,u_passwd=passwd)
        if user:
            request.session['name'] = username
            # request.session.set_expiry(600)
            return redirect('one:home_logined')
        return render(request, 'login.html', context={'mes': '用户名/密码错误'})


def home_logined(request):
    status = request.session.get('name')
    if status:
        user = User.objects.get(u_name=status)

        page = int(request.GET.get('page', 2))
        per_page = int(request.GET.get('per_page', 10))
        movies = Movies.objects.all()
        paginator = Paginator(movies, per_page)
        page_object = paginator.page(page)

        swipers = Swiper.objects.all()
        data = {
            'user': user,
            'page_object': page_object,
            'page_range': paginator.page_range,
            'swipers': swipers,
        }
        return render(request, 'home_logined.html', context=data)
    else:
        return render(request, 'login.html')


def save_movies(request):
    for i in range(1, 100):
        url = r"https://www.vmovier.com/apiv3/post/getPostInCate?cateid=0&p=%d" % i
        datas = requests.get(url).json()
        for i in datas['data']:
            movie = Movies()
            movie.postid = i['postid']
            movie.title = i['title']
            movie.image = i['image']
            movie.like_num = i['like_num']
            movie.request_url = i['request_url']
            movie.save()
    return HttpResponse('success!')


def save_swipers(request):
    url = r'https://www.vmovier.com/apiv3/index/getBanner'
    datas = requests.get(url).json()
    for i in datas['data']:
        swiper = Swiper()
        swiper.image = i['image']
        swiper.save()
    return HttpResponse('success!')