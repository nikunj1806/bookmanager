from rest_framework import serializers
from .models import Loan
from books.serializers import BookSerializer
from users.models import User
from books.models import Book
class LoanSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), write_only=True, source='book')

    class Meta:
        model = Loan
        fields = ['id', 'member', 'book', 'book_id', 'loan_date', 'due_date', 'return_date', 'status', 'overdue_days']
        read_only_fields = ['status', 'overdue_days']

    overdue_days = serializers.SerializerMethodField()

    def get_overdue_days(self, obj):
        return obj.overdue_days()
