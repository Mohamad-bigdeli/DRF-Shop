from django_elasticsearch_dsl import Document, fields, Index
from django.conf import settings
from ..models import Category


CATEGORY_INDEX = Index("categories")

CATEGORY_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=0,
    analysis={
        "analyzer": {
            "edge_ngram_analyzer": {
                "type": "custom",
                "tokenizer": "edge_ngram_tokenizer",
                "filter": ["lowercase"]
            }
        },
        "tokenizer": {
            "edge_ngram_tokenizer": {
                "type": "edge_ngram",
                "min_gram": 2,
                "max_gram": 10,
                "token_chars": ["letter", "digit"]
            }
        }
    }
)

@CATEGORY_INDEX.doc_type
class CategoryDocument(Document):
    
    title = fields.TextField(
        analyzer="edge_ngram_analyzer", 
        search_analyzer="standard"
    )
    slug = fields.TextField()

    class Django:
        model = Category
        fields = [
            "created",
            "updated"
        ]