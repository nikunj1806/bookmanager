from rest_framework import serializers

from books.models import Book
from books.serializers import BookSerializer

from .models import Payment


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
