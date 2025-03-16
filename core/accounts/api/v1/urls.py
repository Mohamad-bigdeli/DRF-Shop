from django.urls import path, include
from .views import (
    ShopUserRelatedView, ShopUserEditView, ShopUserRegisterView, ShopUserChangePasswordView,
    ShopUserForgotPasswordEmailView, 
)

app_name = "api-v1"

urlpatterns = [
    path("user/", ShopUserRelatedView.as_view(), name="user"),
    path("user/edit/", ShopUserEditView.as_view(), name="user-edit"),
    path("user/register/", ShopUserRegisterView.as_view(), name="register"),
    path("user/change-password/", ShopUserChangePasswordView.as_view(), name="change-password"),
    path("user/forgot-password-email/", ShopUserForgotPasswordEmailView.as_view(), name="forgot-password-email"),
    # path("user/forgot-password-phone/", ForgotPasswordPhoneView.as_view(), name="forgot-password-phone")
]