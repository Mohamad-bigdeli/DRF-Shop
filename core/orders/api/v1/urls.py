from django.urls import path
from .views import ShopUserOrdersListView

app_name = "api-v1"

urlpatterns = [
    path("user/orders/", ShopUserOrdersListView.as_view(), name="user-orders")
]