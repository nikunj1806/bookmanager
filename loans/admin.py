from django.contrib import admin
from .models import Loan

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('book', 'member', 'loan_date', 'due_date', 'return_date', 'status')
    list_filter = ('status',)
    search_fields = ('book__title', 'member__username')
