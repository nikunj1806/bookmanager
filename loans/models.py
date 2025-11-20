from django.db import models
from django.utils import timezone
from users.models import User
from books.models import Book

class Loan(models.Model):
    STATUS_ACTIVE = 'active'
    STATUS_RETURNED = 'returned'
    STATUS_OVERDUE = 'overdue'

    STATUS_CHOICES = (
        (STATUS_ACTIVE, 'Active'),
        (STATUS_RETURNED, 'Returned'),
        (STATUS_OVERDUE, 'Overdue'),
    )

    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name='loans')
    store = models.ForeignKey(
        "stores.Store",
        on_delete=models.PROTECT,
        related_name="loans",
        null=True,
        blank=True,
    )
    store_inventory = models.ForeignKey(
        "stores.StoreInventory",
        on_delete=models.PROTECT,
        related_name="loans",
        null=True,
        blank=True,
    )
    loan_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    fine_calculated = models.BooleanField(default=False)

    def is_overdue(self):
        if self.return_date:
            return self.return_date > self.due_date
        return timezone.localdate() > self.due_date

    def overdue_days(self):
        if self.return_date:
            delta = self.return_date - self.due_date
        else:
            delta = timezone.localdate() - self.due_date
        return max(delta.days, 0)
