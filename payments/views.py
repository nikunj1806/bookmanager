from rest_framework import generics
from rest_framework.views import APIView
from .models import Payment
from .serializers import PaymentSerializer
from users.permissions import IsMemberUser
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta, timezone
from decimal import Decimal, InvalidOperation
from books.models import Book

class MemberPaymentListView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsMemberUser]
    def get_queryset(self):
        queryset = Payment.objects.select_related("member", "loan").order_by("-date").filter(member=self.request.user)
        return queryset

class MemberMembershipPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsMemberUser]

    def post(self, request):
        description = request.data.get("description") or "Membership payment"
        latest = (
            Payment.objects.filter(
                member=request.user,
                payment_type=Payment.PAYMENT_TYPE_MEMBERSHIP,
            )
            .order_by("-date")
            .first()
        )
        if latest and (latest.date + timedelta(days=30)) > timezone.now():
            return Response(
                {"detail": "Membership is already active. Renewal available after 30 days."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment = Payment.objects.create(
            member=request.user,
            amount=Decimal("200.00"),
            description=description,
            payment_type=Payment.PAYMENT_TYPE_MEMBERSHIP,
        )
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MemberBuyBookPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsMemberUser]

    def post(self, request):
        book_id = request.data.get("book_id")
        amount = request.data.get("amount")
        if not book_id:
            return Response({"detail": "book_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            amount = Decimal(amount)
        except (TypeError, ValueError, InvalidOperation):
            return Response({"detail": "Invalid amount."}, status=status.HTTP_400_BAD_REQUEST)

        if amount <= 0:
            return Response({"detail": "Amount must be positive."}, status=status.HTTP_400_BAD_REQUEST)

        payment = Payment.objects.create(
            member=request.user,
            amount=amount,
            description=request.data.get("description") or f"Purchase of {book.title}",
            payment_type=Payment.PAYMENT_TYPE_BUY,
            book=book,
        )
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)