from django.db import models
from django.db.models import Sum

from login.models import User


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        indexes = [models.Index(fields=["name"])]



class Product(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["price"]),
        ]


class Order(models.Model):
    class Status(models.TextChoices):
        CREATED = "CREATED", "Created"
        PAID = "PAID", "Paid"
        CANCELLED = "CANCELLED", "Cancelled"

    user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    items = models.ManyToManyField(Product)
    status = models.CharField(choices=Status.choices, default=Status.CREATED, max_length=10)

    @property
    def products_count(self):
        return self.items.count()

    @property
    def total_price(self):
        value = self.items.aggregate(Sum("price"))["price__sum"]
        return (value if value is not None else 0.0)

    def __str__(self):
        return f"Order {self.id}, {self.user.username}, {self.status}"

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["status"]),
        ]


