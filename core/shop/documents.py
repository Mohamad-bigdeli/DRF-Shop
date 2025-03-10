from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Product, Category, ProductFeature

@registry.register_document
class ProductDocument(Document):

    category = fields.ObjectField(properties={"title": fields.TextField(),})
    features = fields.NestedField(properties={"title": fields.TextField(),"value": fields.TextField(),})

    class Index:
        name = 'products'  
        settings = {
            'number_of_shards': 1,  
            'number_of_replicas': 0, 
        }

    class Django:
        model = Product 
        fields = [
            "title",
            "description", 
            "final_price"
        ]
        related_models = [Category, ProductFeature]

    def get_queryset(self):
        return super().get_queryset().select_related("category").prefetch_related("features")

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Category):
            return related_instance.products.all()
        elif isinstance(related_instance, ProductFeature):
            return related_instance.product