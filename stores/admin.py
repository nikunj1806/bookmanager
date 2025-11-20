from django.contrib import admin

from .models import Store, StoreInventory, StoreStaff


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "manager")
    search_fields = ("name", "location")
    list_filter = ("location",)


@admin.register(StoreStaff)
class StoreStaffAdmin(admin.ModelAdmin):
    list_display = ("store", "user", "role", "assigned_at")
    list_filter = ("role", "store")
    search_fields = ("store__name", "user__username")


@admin.register(StoreInventory)
class StoreInventoryAdmin(admin.ModelAdmin):
    list_display = (
        "store",
        "book",
        "total_copies",
        "available_copies",
        "applied_for_sale",
        "copies_for_sale",
        "sale_price",
        "updated_at",
    )
    list_filter = ("store",)
    search_fields = ("store__name", "book__title")

