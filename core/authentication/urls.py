from django.urls import path, include

app_name = "accounts"

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("api-auth/", include("rest_framework.urls")),
]