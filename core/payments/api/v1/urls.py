from django.urls import path
from .views import PaymentVerifyView, PaymentRequestView

app_name = "api-v1"

urlpatterns = [
    path("payment-request/", PaymentRequestView.as_view(), name="payment-request"),
    path("payment-verify/", PaymentVerifyView.as_view(), name="payment-verify")
]