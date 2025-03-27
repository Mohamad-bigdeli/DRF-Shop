from django.urls import path
from .views import OrderCreateView

app_name = "api-v1"

urlpatterns = [
    path("create/", OrderCreateView.as_view(), name="order-create"),
]
