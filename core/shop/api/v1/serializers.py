from rest_framework import serializers
from ...models import Category, ProductImage, ProductFeature, Product
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from ...documents import ProductDocument, CategoryDocument


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
    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)
    absolute_url = serializers.SerializerMethodField()

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
            "relative_url",
            "absolute_url",
            "created",
            "updated",
        ]
        read_only_fields = ["final_price"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get("request")
        rep["category"] = CategorySerializer(
            instance.category, context={"request": request}
        ).data
        return rep

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        if not request:
            return None
        return request.build_absolute_uri(obj.get_absolute_api_url())

    def create(self, validated_data):
        images = validated_data.pop("images")
        features = validated_data.pop("features")
        product = Product.objects.create(**validated_data)
        for image in images:
            ProductImage.objects.create(product=product, **image)
        for feature in features:
            ProductFeature.objects.create(product=product, **feature)
        return product

    def update(self, instance, validated_data):
        images = validated_data.pop("images", [])
        features = validated_data.pop("features", [])
        instance = super().update(instance, validated_data)
        instance.images.all().delete()
        instance.features.all().delete()
        for image in images:
            ProductImage.objects.create(product=instance, **image)
        for feature in features:
            ProductFeature.objects.create(product=instance, **feature)
        return instance


class ProductDocumentSerializer(DocumentSerializer):

    images = ProductImageSerializer(many=True, read_only=True)
    features = ProductFeatureSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)

    class Meta:
        document = ProductDocument
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
            "relative_url",
            "created",
            "updated",
        ]
        read_only_fields = ["final_price"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get("request")
        if "category" in rep and isinstance(rep["category"], dict):
            rep["category"] = CategorySerializer(
                rep["category"], context={"request": request}
            ).data

        if "features" in rep and isinstance(rep["features"], list):
            rep["features"] = [
                ProductFeatureSerializer(feature, context={"request": request}).data
                for feature in rep["features"]
            ]

        if "images" in rep and isinstance(rep["images"], list):
            rep["images"] = [
                ProductImageSerializer(image, context={"request": request}).data
                for image in rep["images"]
            ]

        return rep


class CategoryDocumentSerializer(DocumentSerializer):

    class Meta:
        document = CategoryDocument
        fields = ["id", "title", "slug", "created", "updated"]
