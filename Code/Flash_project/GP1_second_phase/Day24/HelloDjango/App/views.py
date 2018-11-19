import logging

from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render


def hello_transaction(request):

    try:
        with transaction.atomic():
            pass
    except Exception as e:
        transaction.rollback()
    else:
        transaction.commit()

    return HttpResponse("Hello")


def welcome_transaction(request):

    save_point = transaction.savepoint()

    try:
        pass
    except Exception as e:

        transaction.savepoint_rollback(save_point)
    else:

        transaction.savepoint_commit(save_point)

    return HttpResponse("Welcome")


def hello_sql(request):

    # defer
    # only
    results = User.objects.raw("select * from USER ")

    return HttpResponse("sql")


def hello_log(request):
    logger = logging.getLogger("my")
    logger.error("haha error")
    return HttpResponse("hello log")

