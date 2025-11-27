from django.db import models
from django.utils import timezone

from books.models import Book
from loans.models import Loan
from users.models import User


class MembershipPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_days = models.PositiveIntegerField(default=30, help_text="Duration in days")
    max_books_allowed = models.PositiveIntegerField(default=5, help_text="Max books a member can borrow at once")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - ${self.price}"

    class Meta:
        ordering = ["price"]


class UserMembership(models.Model):
    STATUS_ACTIVE = "active"
    STATUS_EXPIRED = "expired"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = (
        (STATUS_ACTIVE, "Active"),
        (STATUS_EXPIRED, "Expired"),
        (STATUS_CANCELLED, "Cancelled"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memberships")
    plan = models.ForeignKey(MembershipPlan, on_delete=models.PROTECT, related_name="subscriptions")
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"

    @property
    def is_active(self):
        return self.status == self.STATUS_ACTIVE and self.end_date > timezone.now()

    class Meta:
        ordering = ["-start_date"]


class Payment(models.Model):
    PAYMENT_TYPE_MEMBERSHIP = "membership"
    PAYMENT_TYPE_BUY = "buy"

    PAYMENT_TYPE_CHOICES = (
        (PAYMENT_TYPE_MEMBERSHIP, "Membership"),
        (PAYMENT_TYPE_BUY, "Book Purchase"),
    )

    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=255, blank=True)
    loan = models.ForeignKey(Loan, on_delete=models.SET_NULL, null=True, blank=True)
    payment_type = models.CharField(
        max_length=20, choices=PAYMENT_TYPE_CHOICES, default=PAYMENT_TYPE_MEMBERSHIP
    )
    book = models.ForeignKey(
        Book, on_delete=models.SET_NULL, null=True, blank=True, related_name="purchases"
    )

    def __str__(self):
        return f"{self.member.username} - {self.amount} ({self.payment_type})"
