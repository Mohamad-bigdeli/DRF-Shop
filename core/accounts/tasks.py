from celery import shared_task
from mail_templated import EmailMessage
from django.conf import settings
from time import sleep


@shared_task
def send_with_email(verification_code, email):
    email_message = EmailMessage(
        "email/forgot_email.tpl",
        {"verification_code": verification_code},
        settings.EMAIL_HOST_USER,
        to=[email],
    )
    email_message.send()


@shared_task
def send_with_phone(verification_code, phone):
    sleep(5)
    # The operation of sending a code to a phone number is done here.
    print(f"verification code : {verification_code} for {phone}")


# def send_with_email(verification_code, email):
#     email_message = EmailMessage(
#         "email/forgot_email.tpl",
#         {"verification_code":verification_code},
#         settings.EMAIL_HOST_USER,
#         to=[email],
#     )
#     email_message.send()

# def send_with_phone(verification_code, phone):
#     sleep(5)
#     # The operation of sending a code to a phone number is done here.
#     print(f"verification code : {verification_code} for {phone}")
