from django.contrib import admin
from .models import Category, Product, ProductFeature, ProductImage

# Register your models here.

class ImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0

class FeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 0

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created', 'updated']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'inventory', 'price', 'discount', 'final_price', 'created', 'updated']
    list_filter = ['created']
    inlines = [ImageInline, FeatureInline]
    