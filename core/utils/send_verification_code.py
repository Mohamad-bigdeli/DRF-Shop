from celery import shared_task
from mail_templated import EmailMessage
from django.conf import settings

@shared_task
def send_with_email(verification_code, email):
    email_message = EmailMessage(
        "email/forgot_email.tpl",
        {"verification_code":verification_code},
        settings.EMAIL_HOST_USER,
        to=[email],
    )
    email_message.send()

def send_with_phone():
    pass