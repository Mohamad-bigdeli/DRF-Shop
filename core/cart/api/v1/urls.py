from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CartViewSet

app_name = "api-v1"

router = DefaultRouter()

router.register(r"cart", CartViewSet, basename="cart")

urlpatterns = []

urlpatterns+=router.urls