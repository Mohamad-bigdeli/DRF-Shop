from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    CustomTokenObtainPairSerializer,
    OtpRequestSerializer,
    OtpVerifySerializer,
)
from rest_framework import generics
from utils.generate_code import generate_code
from accounts.tasks import send_with_phone
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

# get custom user model
User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class OtpRequestView(generics.GenericAPIView):

    serializer_class = OtpRequestSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data["phone"]

        try:
            otp_code = str(generate_code())
            cache.set(phone, otp_code, timeout=120)
            send_with_phone.delay(otp_code, phone)

        except Exception:
            return Response(
                {"detail": "The operation was not performed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(
            {"detail": "Send otp code successfully"}, status=status.HTTP_200_OK
        )


class OtpVerifyView(generics.GenericAPIView):

    serializer_class = OtpVerifySerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data["phone"]
        otp_code = serializer.validated_data["otp_code"]

        try:
            otp_cache = cache.get(phone)
            if not otp_cache:
                return Response(
                    {
                        "detail": "The one-time code has expired or invalid phone. Request again."
                    }
                )
            if otp_cache == otp_code:
                user = (
                    User.objects.filter(phone=phone).first()
                    if User.objects.filter(phone=phone).first()
                    else None
                )
                if user:
                    user.is_verified = True
                    user.save()
                    return Response(
                        {
                            "detail": "The one-time code is correct and the user was verified."
                        },
                        status=status.HTTP_200_OK,
                    )
                cache.delete(phone)
                return Response(
                    {"detail": "The one-time code is correct."},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"detail": "The one-time code is wrong!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception:
            return Response(
                {"detail": "The operation was not performed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
