from django.db import models
from django.utils import timezone

from books.models import Book
from loans.models import Loan
from users.models import User


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
