from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from books.models import Book
from books.serializers import BookSerializer
from payments.models import Payment
from stores.models import Store, StoreInventory
from users.models import User

from .models import Loan


class LoanSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    member = serializers.PrimaryKeyRelatedField(read_only=True)
    store = serializers.PrimaryKeyRelatedField(read_only=True)
    store_name = serializers.CharField(source="store.name", read_only=True)

    class Meta:
        model = Loan
        fields = [
            "id",
            "member",
            "book",
            "store",
            "store_name",
            "store_inventory",
            "loan_date",
            "due_date",
            "return_date",
            "status",
            "overdue_days",
        ]
        read_only_fields = [
            "member",
            "book",
            "store",
            "store_name",
            "store_inventory",
            "loan_date",
            "status",
            "overdue_days",
        ]

    overdue_days = serializers.SerializerMethodField()

    def get_overdue_days(self, obj):
        return obj.overdue_days()


class BorrowRequestSerializer(serializers.Serializer):
    member_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="member"
    )
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), source="book"
    )
    store_id = serializers.PrimaryKeyRelatedField(
        queryset=Store.objects.all(), source="store"
    )
    due_date = serializers.DateField(required=False)

    def validate(self, attrs):
        member = attrs["member"]
        book = attrs["book"]
        store = attrs["store"]

        try:
            inventory = StoreInventory.objects.get(store=store, book=book)
        except StoreInventory.DoesNotExist:
            raise serializers.ValidationError(
                "The selected store does not have this book in inventory."
            )

        if inventory.available_copies <= 0:
            raise serializers.ValidationError("Book is currently unavailable at this store.")

        if Loan.objects.filter(
            member=member,
            book=book,
            store=store,
            status=Loan.STATUS_ACTIVE,
        ).exists():
            raise serializers.ValidationError(
                "Member already has an active loan for this book at this store."
            )

        latest_membership = (
            member.payments.filter(payment_type=Payment.PAYMENT_TYPE_MEMBERSHIP)
            .order_by("-date")
            .first()
        )
        if not latest_membership:
            raise serializers.ValidationError(
                "Member does not have an active membership payment."
            )

        membership_valid_until = latest_membership.date + timedelta(days=30)
        if membership_valid_until.date() < timezone.localdate():
            raise serializers.ValidationError(
                "Membership payment has expired. Please renew membership."
            )

        attrs.setdefault("due_date", timezone.localdate() + timedelta(days=14))
        attrs["inventory"] = inventory
        return attrs
