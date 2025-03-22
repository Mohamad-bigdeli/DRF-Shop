from rest_framework import serializers
from ...models import Review
from shop.models import Product
from django.contrib.auth import get_user_model

# get custom user model 
User = get_user_model()

class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title"]

class ShopUserReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["id", "phone", "email"]

class ReviewRelatedSerializer(serializers.ModelSerializer):

    product = ProductReviewSerializer()
    user = ShopUserReviewSerializer()

    class Meta:
        model = Review
        fields = [
            "id",
            "product",
            "user", 
            "rating",
            "comment",
            "approved",
            "created",
            "updated"
        ]

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["product", "rating", "comment"]