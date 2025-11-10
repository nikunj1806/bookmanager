from django.db import models
from django.utils import timezone
from users.models import User
from loans.models import Loan

class Payment(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=255, blank=True)
    loan = models.ForeignKey(Loan, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.member.username} - {self.amount}"
