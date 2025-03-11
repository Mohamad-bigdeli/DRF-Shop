from rest_framework import serializers
from ...models import Category , ProductImage, ProductFeature, Product
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from ...documents import ProductDocument


class CategorySerializer(serializers.ModelSerializer):

    slug = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "title", "slug", "created", "updated"]

class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ["id", "image"]

class ProductFeatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductFeature
        fields = ["id", "title", "value"]

class ProductSerializer(serializers.ModelSerializer):

    images = ProductImageSerializer(many=True)
    features = ProductFeatureSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "title",
            "images",
            "description",
            "features",
            "inventory",
            "price",
            "discount",
            "final_price",
            "created",
            "updated"
        ]
        read_only_fields = ["final_price"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get("request")
        rep["category"] = CategorySerializer(instance.category, context={"request": request}).data
        return rep

    def create(self, validated_data):
        images = validated_data.pop('images')
        features = validated_data.pop('features')
        product = Product.objects.create(**validated_data)
        for image in images:
            ProductImage.objects.create(product=product, **image)
        for feature in features:
            ProductFeature.objects.create(product=product, **feature)
        return product

def update(self, instance, validated_data):
    images = validated_data.pop('images', [])  
    features = validated_data.pop('features', []) 
    instance = super().update(instance, validated_data)
    instance.images.all().delete()
    instance.features.all().delete()
    for image in images:
        ProductImage.objects.create(product=instance, **image)
    for feature in features:
        ProductFeature.objects.create(product=instance, **feature)
    return instance

class ProductDocumentSerializer(DocumentSerializer):
    
    class Meta:
        document = ProductDocument
        fields = [
            "id",
            "title",
            "description",
            "final_price",
            "category.title",
            "features.value",
        ]