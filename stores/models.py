from django.conf import settings
from django.db import models

from books.models import Book


class Store(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_stores",
    )
    staff = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="StoreStaff",
        related_name="stores",
        blank=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class StoreStaff(models.Model):
    ROLE_ADMIN = "admin"
    ROLE_STAFF = "staff"

    ROLE_CHOICES = (
        (ROLE_ADMIN, "Admin"),
        (ROLE_STAFF, "Staff"),
    )

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="store_staff")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="store_memberships"
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_STAFF)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("store", "user")
        verbose_name_plural = "store staff"

    def __str__(self):
        return f"{self.user} @ {self.store} ({self.role})"


class StoreInventory(models.Model):
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name="inventory_items"
    )
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="store_inventories"
    )
    total_copies = models.PositiveIntegerField(default=0)
    available_copies = models.PositiveIntegerField(default=0)
    applied_for_sale = models.BooleanField(default=False)
    copies_for_sale = models.PositiveIntegerField(default=0)
    sale_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Price per copy when sale copies are available.",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("store", "book")
        verbose_name_plural = "store inventory"

    def __str__(self):
        return f"{self.book} @ {self.store}"

