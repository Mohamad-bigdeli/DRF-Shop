from django.urls import path
from .views import ReviewRelatedView

app_name = "api-v1"

urlpatterns = [
    path("products/<pk>/reviews/", ReviewRelatedView.as_view(), name="reviews")
]