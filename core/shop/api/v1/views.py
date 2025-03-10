from rest_framework import viewsets
from ...models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, ProductDocumentSerializer
from rest_framework.permissions import IsAdminUser, SAFE_METHODS, AllowAny
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from ...documents import ProductDocument
from django_elasticsearch_dsl_drf.filter_backends import FilteringFilterBackend, OrderingFilterBackend, SearchFilterBackend

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

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser()]

class ProductDocumentViewSet(DocumentViewSet):

    document = ProductDocument
    serializer_class = ProductDocumentSerializer

    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend, 
        SearchFilterBackend
    ]

    search_fields = (
        "title",
        "description",
        "category.title",
        "features.value"
    )

    filter_fields = {
        "final_price" : "final_price" 
    }

    ordering_fields = {
        "final_price": "final_price", 
        "title": "title",
    }