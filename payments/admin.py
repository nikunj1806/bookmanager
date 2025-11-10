from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('member', 'amount', 'date', 'loan')
    search_fields = ('member__username',)
