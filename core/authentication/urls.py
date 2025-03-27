from django.urls import path, include

app_name = "authentication"

urlpatterns = [
    path("api/v1/", include("authentication.api.v1.urls")),
    path("api-auth/", include("rest_framework.urls")),
]
