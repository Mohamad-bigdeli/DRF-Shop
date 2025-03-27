from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import (
    ReviewRelatedSerializer,
    ReviewCreateSerializer,
    ReviewUpdateSerializer,
)
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ...models import Review


class ReviewCreateListView(ListCreateAPIView):

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


class ReviewUpdateDestroyView(RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        if self.request.method in SAFE_METHODS:
            return Review.objects.all()
        return Review.objects.filter(user=self.request.user)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer(self, *args, **kwargs):
        if self.request.method in SAFE_METHODS:
            return ReviewRelatedSerializer(*args, **kwargs)
        return ReviewUpdateSerializer(*args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user != instance.user:
            return Response(
                {"detail": "You do not have permission to edit this comment."},
                status=status.HTTP_403_FORBIDDEN,
            )

        allowed_fields = ["comment", "rating"]
        for field in request.data:
            if field not in allowed_fields:
                return Response(
                    {"detail": "You can only change the comment and rating fields."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return super().partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user != instance.user:
            return Response(
                {"detail": "You do not have permission to delete this comment."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().destroy(request, *args, **kwargs)
