from rest_framework.generics import ListCreateAPIView
from .serializers import ReviewRelatedSerializer, ReviewCreateSerializer
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from ...models import Review


class ReviewRelatedView(ListCreateAPIView):

    queryset = Review.objects.filter(approved=True).all()

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer(self, *args, **kwargs):
        if self.request.method in SAFE_METHODS:
            return ReviewRelatedSerializer(*args, **kwargs)
        return ReviewCreateSerializer(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    

    
    

    