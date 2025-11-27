from django.contrib import admin
from .models import Payment, MembershipPlan, UserMembership


@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days', 'max_books_allowed', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    list_editable = ('is_active', 'price')
    ordering = ('price',)


@admin.register(UserMembership)
class UserMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'status', 'is_active')
    list_filter = ('status', 'plan')
    search_fields = ('user__username', 'user__email', 'plan__name')
    raw_id_fields = ('user',)
    date_hierarchy = 'start_date'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('member', 'amount', 'date', 'loan', 'payment_type')
    list_filter = ('payment_type',)
    search_fields = ('member__username',)
