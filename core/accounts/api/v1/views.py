from rest_framework import generics, mixins, status
from rest_framework.response import Response
from .serializers import (ShopUserRelatedSerializer, ShopUserUpdateSerializer,
            ShopUserRegisterSerializer, ShopUserChangePasswordSerializer, 
            ShopUserForgotPasswordEmailSerializer, 
        )
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from utils.generate_code import generate_code
from django.core.cache import cache
from utils.send_verification_code import send_with_email, send_with_phone

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
        data = {
                "message": "User registered successfully.",
                "user_id": user.id,
                "email": user.email,
                "phone": user.phone,
            },

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
            return Response({
                "detail": "The old password is wrong!"
            }, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data["new_password"])  
        user.save()

        return Response({
            "detail": "Change password successfully"
        }, status=status.HTTP_200_OK)

class ShopUserForgotPasswordEmailView(generics.GenericAPIView):

    serializer_class = ShopUserForgotPasswordEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.filter(email=email).first()

        if user:
            verification_code = generate_code()
            cache.set(f"email-{user.id}", verification_code, timeout=120)

            send_with_email.delay(verification_code, email)
            
            return Response({"detail":"Send verification code successfully"}, status=status.HTTP_200_OK)
        return Response({"detail":"User dose not exist!"}, status=status.HTTP_404_NOT_FOUND)