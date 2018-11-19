from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email(receive):

    subject = 'yes'
    message = 'really'
    form_email = 'rongjiawei1204@163.com'
    recipient_list = (receive,)
    send_mail(subject=subject, message=message,from_email=form_email,recipient_list=recipient_list)
