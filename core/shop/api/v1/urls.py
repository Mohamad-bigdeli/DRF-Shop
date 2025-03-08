from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet

app_name = "api-v1"

router = DefaultRouter()

router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"products", ProductViewSet, basename="products")

urlpatterns = []

urlpatterns+=router.urls