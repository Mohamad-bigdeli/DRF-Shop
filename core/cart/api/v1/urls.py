from django.urls import path
from . import views 

app_name = "api-v1"

urlpatterns = [
    path("add-item/", views.AddItemToCartView.as_view(), name="add-item"),
    path("update-item/", views.UpdateItemInCartView.as_view(), name="update-item"),
    path("items/", views.GetCartItemsView.as_view(), name="items"),
    path("remove-item/", views.RemoveItemFromCartView.as_view(), name="remove-item"),
    path("clear/", views.ClearCartView.as_view(), name="clear")
]