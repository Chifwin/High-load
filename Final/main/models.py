from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User

from .utils import TimestampMixin


# Create your models here.

class Category(TimestampMixin):
    name = models.CharField(max_length=255)
    parent_id = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, blank=True, verbose_name="Parent category")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(TimestampMixin):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=18, decimal_places=2)
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


class Order(TimestampMixin):
    class Status(models.TextChoices):
        CREATED = "created", "Created"
        IN_PROGRESS = "in_progress", "In progress"
        DONE = "done", "Done"
        CANCELED = "canceled", "Canceled"

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    order_status = models.CharField(max_length=20, choices=Status.choices, default=Status.CREATED)
    total_amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if self.pk:
            self.total_amount = sum(item.price for item in self.items.all())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.pk} for {self.user_id}"

    class Meta:
        ordering = ["-created_at"]


class OrderItem(TimestampMixin):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=18, decimal_places=2)

    def save(self, *args, **kwargs):
        self.price = self.product_id.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_id} in quantity {self.quantity} in order #{self.order_id.id}"


class Payment(TimestampMixin):
    class PaymentMethod(models.TextChoices):
        CASH = "cash", "Cash"
        CARD = "card", "Card"
        BANK = "bank", "Bank"

    class PaymentStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"

    order_id = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    payment_method = models.CharField(max_length=50, choices=PaymentMethod.choices)
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)

    def __str__(self):
        return f"Payment for order #{self.order_id.id}"


class ShoppingCart(TimestampMixin):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Shopping cart for {self.user_id}"


class CartItem(TimestampMixin):
    cart_id = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name="items")
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product_id} in queantity {self.quantity} in cart for {self.cart.user_id}"

    class Meta:
        constraints = [models.UniqueConstraint(fields=["cart_id", "product_id"], name="unique_cart_item")]


class Wishlist(TimestampMixin):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wishlist")

    def __str__(self):
        return f"Wishlist for {self.user_id}"


class WishlistItem(TimestampMixin):
    wishlist_id = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name="items")
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product_id} in wishlist for {self.wishlist.user_id}"

    class Meta:
        constraints = [models.UniqueConstraint(fields=["wishlist_id", "product_id"], name="unique_wishlist_item")]
