from django.urls import path
from .views import ReviewCreateListView, ReviewUpdateDestroyView

app_name = "api-v1"

urlpatterns = [
    path("products/<pk>/reviews/", ReviewCreateListView.as_view(), name="reviews"),
    path("reviews/<pk>", ReviewUpdateDestroyView.as_view(), name="reviews-detail")
]