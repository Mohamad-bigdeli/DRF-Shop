from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    ProductViewSet,
    ProductDocumentViewSet,
    CategoryDocumentViewSet,
)

app_name = "api-v1"

router = DefaultRouter()

router.register(r"categories", CategoryViewSet, basename="categories"),
router.register(r"products", ProductViewSet, basename="products"),

urlpatterns = [
    path(
        "products/",
        ProductDocumentViewSet.as_view({"get": "list"}),
        name="products-search",
    ),
    path(
        "categories/",
        CategoryDocumentViewSet.as_view({"get": "list"}),
        name="categories-search",
    ),
]

urlpatterns += router.urls
