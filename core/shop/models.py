from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    """
    The Category model is used to categorize products.
    Each category has a unique title and a slug.
    """

    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Override the save method to automatically generate the slug from the title.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Product(models.Model):
    """
    The Product model stores information about products.
    Each product is associated with a category and can have a discount.
    """

    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.DO_NOTHING
    )
    description = models.TextField()
    inventory = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    final_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Override the save method to automatically calculate and save the final price.
        """
        if self.discount > 0:
            self.final_price = self.price * (1 - self.discount / 100)
        else:
            self.final_price = self.price
        super().save(*args, **kwargs)

    def get_absolute_api_url(self):
        return reverse("shop:api-v1:products-detail", kwargs={"pk": self.pk})


class ProductImage(models.Model):
    """
    The ProductImage model is used to store images related to a product.
    Each product can have multiple images.
    """

    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="product_images/")

    def __str__(self):
        return f"Image for {self.product.title}"


class ProductFeature(models.Model):
    """
    The ProductFeature model is used to store specific features of a product.
    Each feature has a name and a value and is associated with a product.
    """

    title = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    product = models.ForeignKey(
        Product, related_name="features", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} : {self.value}"
