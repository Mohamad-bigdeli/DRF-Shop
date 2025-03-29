from django_elasticsearch_dsl import Document, fields, Index
from ..models import Product


PRODUCT_INDEX = Index("products")

PRODUCT_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=0,
    analysis={
        "analyzer": {
            "edge_ngram_analyzer": {
                "type": "custom",
                "tokenizer": "edge_ngram_tokenizer",
                "filter": ["lowercase"],
            }
        },
        "tokenizer": {
            "edge_ngram_tokenizer": {
                "type": "edge_ngram",
                "min_gram": 2,
                "max_gram": 10,
                "token_chars": ["letter", "digit"],
            }
        },
    },
)


@PRODUCT_INDEX.doc_type
class ProductDocument(Document):
    title = fields.TextField(analyzer="edge_ngram_analyzer", search_analyzer="standard")
    category = fields.ObjectField(
        properties={
            "title": fields.TextField(
                analyzer="edge_ngram_analyzer", search_analyzer="standard"
            ),
            "slug": fields.TextField(),
        }
    )
    features = fields.NestedField(
        properties={"title": fields.TextField(), "value": fields.TextField()}
    )

    class Django:
        model = Product
        fields = [
            "description",
            "inventory",
            "price",
            "discount",
            "final_price",
            "created",
            "updated",
        ]
