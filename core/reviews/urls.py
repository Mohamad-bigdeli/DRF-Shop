from django.urls import path, include

app_name = "reviews"

urlpatterns = [
    path("api/v1/", include("reviews.api.v1.urls"))
]