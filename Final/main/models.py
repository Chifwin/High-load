from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User

from .utils import TimestampMixin


# Create your models here.

class Category(TimestampMixin):
    name = models.CharField(max_length=255)
    parent_id = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Parent category"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(TimestampMixin):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Review(TimestampMixin):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(limit_value=5)])

    def __str__(self):
        return f"Review for {self.product_id.name} by {self.user_id.username}"

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        constraints = [models.UniqueConstraint(fields=["product_id", "user_id"], name="unique_user_review")]
        # indexes = [models.Index(fields=["product_id", "user_id"])]
