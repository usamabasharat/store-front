from django.core.cache import cache
from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from templated_mail.mail import BaseEmailMessage
from django.shortcuts import render
from .tasks import notify_customer
import requests
import environ

env = environ.Env()
environ.Env.read_env()


def say_hello(request):
  # Background task
  notify_customer.delay('hello')

  try:
    # Templated Email
    message = BaseEmailMessage(
        template_name='emails/hello.html', context={'name': 'Usama'})
    message.send([env('EMAIL_TO')])

    # Email with attachment
    message = EmailMessage('Test Subject', 'Email Testing body',
                           env('DEFAULT_FROM_EMAIL'), [env('EMAIL_TO')])
    message.attach_file('playground/static/images/food.jpeg')
    message.send()

    # Simple Email
    send_mail('Test Subject', 'Email Testing body',
              env('DEFAULT_FROM_EMAIL'), [env('EMAIL_TO')])

    # Email to Admins
    mail_admins('Test admin subject', 'message', html_message='message')
  except BadHeaderError:
    pass
  return render(request, 'hello.html', {'name': 'Usama'})


@cache_page(10)
def trying_cache(request):
  response = requests.get('https://httpbin.org/delay/2')
  data = response.json()

  return render(request, 'hello.html', {'name': data})


class HelloView(APIView):
  @method_decorator(cache_page(10))
  def get(self, request):
    response = requests.get('https://httpbin.org/delay/2')
    data = response.json()

    return render(request, 'hello.html', {'name': data})
