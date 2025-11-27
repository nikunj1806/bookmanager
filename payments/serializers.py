from rest_framework import serializers

from books.models import Book
from books.serializers import BookSerializer

from .models import Payment, MembershipPlan, UserMembership


class MembershipPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipPlan
        fields = [
            "id",
            "name",
            "description",
            "price",
            "duration_days",
            "max_books_allowed",
        ]


class UserMembershipSerializer(serializers.ModelSerializer):
    plan = MembershipPlanSerializer(read_only=True)
    plan_id = serializers.PrimaryKeyRelatedField(
        queryset=MembershipPlan.objects.filter(is_active=True),
        source="plan",
        write_only=True,
    )
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = UserMembership
        fields = [
            "id",
            "user",
            "plan",
            "plan_id",
            "start_date",
            "end_date",
            "status",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["user", "start_date", "end_date", "status", "is_active", "created_at"]


class PaymentSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        source="book",
        write_only=True,
        required=False,
    )

    class Meta:
        model = Payment
        fields = [
            "id",
            "member",
            "amount",
            "date",
            "description",
            "loan",
            "payment_type",
            "book",
            "book_id",
        ]
        read_only_fields = ["loan", "member", "date", "payment_type"]
