from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from ...models import Order
from .serializers import ShopUserOrdersRelatedSerializer

class ShopUserOrdersListView(generics.ListAPIView):

    serializer_class = ShopUserOrdersRelatedSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        order = Order.objects.select_related("payment").prefetch_related("items__product").filter(user=self.request.user)
        return order