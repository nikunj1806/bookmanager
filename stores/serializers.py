from django.db import transaction
from rest_framework import serializers

from books.models import Book
from users.models import User

from .models import Store, StoreInventory, StoreStaff


class StoreStaffSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    user_username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = StoreStaff
        fields = [
            "id",
            "store",
            "user",
            "user_username",
            "role",
            "assigned_at",
        ]
        read_only_fields = ["assigned_at"]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        instance = getattr(self, "instance", None)
        store = attrs.get("store")
        if store is None and instance is not None:
            store = instance.store

        user = attrs.get("user")
        if user is None and instance is not None:
            user = instance.user

        if (
            store
            and user
            and store.manager_id
            and store.manager_id == user.id
            and attrs.get("role") == StoreStaff.ROLE_STAFF
        ):
            raise serializers.ValidationError(
                {"role": "Store managers must retain admin role within the store."}
            )
        return attrs


class StoreInventorySerializer(serializers.ModelSerializer):
    store = serializers.PrimaryKeyRelatedField(queryset=Store.objects.all())
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    book_title = serializers.CharField(source="book.title", read_only=True)

    class Meta:
        model = StoreInventory
        fields = [
            "id",
            "store",
            "book",
            "book_title",
            "total_copies",
            "available_copies",
            "applied_for_sale",
            "copies_for_sale",
            "sale_price",
            "updated_at",
        ]
        read_only_fields = ["updated_at"]

    def validate(self, attrs):
        attrs = super().validate(attrs)

        instance = getattr(self, "instance", None)

        total_copies = attrs.get("total_copies")
        if total_copies is None and instance is not None:
            total_copies = instance.total_copies

        available_copies = attrs.get("available_copies")
        if available_copies is None and instance is not None:
            available_copies = instance.available_copies

        if total_copies is not None and total_copies < 0:
            raise serializers.ValidationError(
                {"total_copies": "Total copies must be zero or greater."}
            )

        if available_copies is not None:
            if available_copies < 0:
                raise serializers.ValidationError(
                    {"available_copies": "Available copies must be zero or greater."}
                )
            if total_copies is not None and available_copies > total_copies:
                raise serializers.ValidationError(
                    {"available_copies": "Available copies cannot exceed total copies."}
                )

        applied_for_sale = attrs.get("applied_for_sale")
        if applied_for_sale is None and instance is not None:
            applied_for_sale = instance.applied_for_sale

        copies_for_sale = attrs.get("copies_for_sale")
        if copies_for_sale is None and instance is not None:
            copies_for_sale = instance.copies_for_sale

        sale_price = attrs.get("sale_price")
        if sale_price is None and instance is not None:
            sale_price = instance.sale_price

        if applied_for_sale:
            if copies_for_sale is None or copies_for_sale <= 0:
                raise serializers.ValidationError(
                    {"copies_for_sale": "Copies for sale must be provided and greater than zero when sale is enabled."}
                )
            if copies_for_sale > (total_copies or 0):
                raise serializers.ValidationError(
                    {"copies_for_sale": "Copies for sale cannot exceed total copies."}
                )
            if sale_price is None or sale_price <= 0:
                raise serializers.ValidationError(
                    {"sale_price": "Sale price must be greater than zero when sale is enabled."}
                )
        else:
            attrs["copies_for_sale"] = 0
            attrs["sale_price"] = None

        return attrs


class StoreSerializer(serializers.ModelSerializer):
    manager = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True,
    )
    manager_username = serializers.CharField(source="manager.username", read_only=True)
    inventory_count = serializers.IntegerField(source="inventory_items.count", read_only=True)

    class Meta:
        model = Store
        fields = [
            "id",
            "name",
            "location",
            "manager",
            "manager_username",
            "inventory_count",
        ]

    @transaction.atomic
    def create(self, validated_data):
        manager = validated_data.get("manager")
        store = super().create(validated_data)
        if manager:
            StoreStaff.objects.get_or_create(
                store=store,
                user=manager,
                defaults={"role": StoreStaff.ROLE_ADMIN},
            )
        return store

    @transaction.atomic
    def update(self, instance, validated_data):
        previous_manager_id = instance.manager_id
        store = super().update(instance, validated_data)
        new_manager = validated_data.get("manager")
        if new_manager and new_manager.id != previous_manager_id:
            StoreStaff.objects.update_or_create(
                store=store,
                user=new_manager,
                defaults={"role": StoreStaff.ROLE_ADMIN},
            )
        if previous_manager_id and previous_manager_id != getattr(new_manager, "id", None):
            StoreStaff.objects.filter(
                store=store, user_id=previous_manager_id, role=StoreStaff.ROLE_ADMIN
            ).update(role=StoreStaff.ROLE_STAFF)
        return store

