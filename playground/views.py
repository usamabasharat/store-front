from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from templated_mail.mail import BaseEmailMessage
from django.shortcuts import render
import environ

env = environ.Env()
environ.Env.read_env()


def say_hello(request):
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