from rest_framework import viewsets
from ...models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, ProductDocumentSerializer, CategoryDocumentSerializer
from rest_framework.permissions import IsAdminUser, SAFE_METHODS, AllowAny
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from ...documents import ProductDocument, CategoryDocument
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
    MultiMatchSearchFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend
)
from .paginations import CustomPagination

class CategoryViewSet(viewsets.ModelViewSet):
    
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser()]

class ProductViewSet(viewsets.ModelViewSet):

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser()]

class ProductDocumentViewSet(DocumentViewSet):

    document = ProductDocument
    serializer_class = ProductDocumentSerializer
    pagination_class = CustomPagination

    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        MultiMatchSearchFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend
    ]

    multi_match_search_fields = {
        "title": {"boost": 4},
        "description": {"boost": 2},
        "category.title": {"boost": 3},
        "features.value": {"boost": 1}
    }

    search_fields = (
        "title", 
        "description",
        "category.title",
        "features.value"
    )

    multi_match_options = {
        "fuzziness": "AUTO",
        "prefix_length": 2,
        "max_expansions": 50
    }

    ordering_fields = {
        "final_price": "final_price",
        "created": "created",
        "updated": "updated"
    }

    filter_fields = {
        "final_price": "final_price",
        "category.title": "category.title",
        "features.value": "features.value"
    }
class CategoryDocumentViewSet(DocumentViewSet):

    document = CategoryDocument
    serializer_class = CategoryDocumentSerializer
    pagination_class = CustomPagination

    filter_backends = [
        OrderingFilterBackend,
        MultiMatchSearchFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend
    ]
    multi_match_search_fields = {
        "title": {"boost": 4},
    }

    search_fields = [
        "title"
    ]

    ordering_fields = {
        "created": "created",
        "updated": "updated"
    }