from rest_framework import generics, mixins, status
from rest_framework.response import Response
from .serializers import (
    ShopUserRelatedSerializer,
    ShopUserUpdateSerializer,
    ShopUserRegisterSerializer,
    ShopUserChangePasswordSerializer,
    ShopUserForgotPasswordEmailSerializer,
    ShopUserForgotPasswordPhoneSerializer,
    ResetPasswordSerializer,
    ProfileRelatedSerializer,
    ProfileUpdateSerializer,
)
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from utils.generate_code import generate_code
from django.core.cache import cache
from ...tasks import send_with_email, send_with_phone
from ...models import Profile

# get custom user model
User = get_user_model()


class ShopUserRelatedView(generics.GenericAPIView, mixins.RetrieveModelMixin):

    serializer_class = ShopUserRelatedSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):

        return get_object_or_404(User, id=self.request.user.id)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ShopUserEditView(generics.GenericAPIView, mixins.UpdateModelMixin):

    serializer_class = ShopUserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ShopUserRegisterView(generics.GenericAPIView):

    serializer_class = ShopUserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = (
            {
                "message": "User registered successfully.",
                "user_id": user.id,
                "email": user.email,
                "phone": user.phone,
            },
        )

        return Response(data, status=status.HTTP_201_CREATED)


class ShopUserChangePasswordView(generics.GenericAPIView):
    serializer_class = ShopUserChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)

    def put(self, request, *args, **kwargs):

        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not user.check_password(serializer.validated_data["old_password"]):
            return Response(
                {"detail": "The old password is wrong!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response(
            {"detail": "Change password successfully"}, status=status.HTTP_200_OK
        )


class ShopUserForgotPasswordEmailView(generics.GenericAPIView):

    serializer_class = ShopUserForgotPasswordEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.filter(email=email).first()

        if user:
            try:
                verification_code = str(generate_code())
                cache.set(f"email-{user.id}", verification_code, timeout=120)
                send_with_email.delay(verification_code, email)
            except Exception:
                return Response(
                    {"detail": "The operation was not performed"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(
                {"detail": "Send verification code successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"detail": "User dose not exist!"}, status=status.HTTP_404_NOT_FOUND
        )


class ForgotPasswordPhoneView(generics.GenericAPIView):

    serializer_class = ShopUserForgotPasswordPhoneSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data["phone"]
        user = User.objects.filter(phone=phone).first()

        if user:
            try:
                verification_code = str(generate_code())
                cache.set(f"phone-{user.id}", verification_code, timeout=120)
                send_with_phone.delay(verification_code, phone)

            except Exception:
                return Response(
                    {"detail": "The operation was not performed"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(
                {"detail": "Send verification code successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"detail": "User dose not exist!"}, status=status.HTTP_404_NOT_FOUND
        )


class ResetPasswordView(generics.GenericAPIView):

    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = (
            serializer.validated_data["email"]
            if serializer.validated_data.get("email")
            else None
        )
        phone = (
            serializer.validated_data["phone"]
            if serializer.validated_data.get("phone")
            else None
        )
        verification_code = serializer.validated_data["verification_code"]
        new_password = serializer.validated_data["new_password"]
        new_password1 = serializer.validated_data["new_password1"]

        if email:
            user = User.objects.filter(email=email).first()
            cache_key = f"email-{user.id}" if user else None
        elif phone:
            user = User.objects.filter(phone=phone).first()
            cache_key = f"phone-{user.id}" if user else None
        if not user:
            return Response(
                {"detail": "User does not exist."}, status=status.HTTP_404_NOT_FOUND
            )

        verification_code_cache = cache.get(cache_key)
        if verification_code != verification_code_cache:
            return Response(
                {"detail": "The code entered is not correct."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif new_password == new_password1:
            user.set_password(new_password)
            user.save()
            cache.delete(cache_key)
            return Response(
                {"detail": "Password set successfully."}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail": "Passwords doesn't match!"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ShopUserDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):

    permission_classes = [IsAuthenticated]

    def get_object(self):
        return User.objects.filter(id=self.request.user.id).first()


class ProfileRelatedView(generics.GenericAPIView, mixins.RetrieveModelMixin):

    serializer_class = ProfileRelatedSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile = Profile.objects.filter(user=self.request.user.id).first()
        return profile

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ProfileUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):

    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile = Profile.objects.filter(user=self.request.user).first()
        return profile

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
