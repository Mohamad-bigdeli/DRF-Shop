from django.urls import path, include
from .views import (
    ShopUserRelatedView, ShopUserEditView, ShopUserRegisterView, ShopUserChangePasswordView
)

app_name = "api-v1"

urlpatterns = [
    path("user/", ShopUserRelatedView.as_view(), name="user"),
    path("user/edit/", ShopUserEditView.as_view(), name="user-edit"),
    path("register/", ShopUserRegisterView.as_view(), name="register"),
    path("user/change-password/", ShopUserChangePasswordView.as_view(), name="change-password")
]