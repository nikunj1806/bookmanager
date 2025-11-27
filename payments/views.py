from rest_framework import generics
from rest_framework.views import APIView
from .models import Payment, MembershipPlan, UserMembership
from .serializers import PaymentSerializer, MembershipPlanSerializer, UserMembershipSerializer
from users.permissions import IsMemberUser
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from django.utils import timezone
from decimal import Decimal, InvalidOperation
from books.models import Book

class MemberPaymentListView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsMemberUser]
    def get_queryset(self):
        queryset = Payment.objects.select_related("member", "book").filter(payment_type=Payment.PAYMENT_TYPE_BUY).order_by("-date").filter(member=self.request.user)
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


class MembershipPlanListView(generics.ListAPIView):
    """List all active membership plans available for users to apply."""
    serializer_class = MembershipPlanSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return MembershipPlan.objects.filter(is_active=True)


class UserMembershipListView(generics.ListAPIView):
    """List current user's memberships."""
    serializer_class = UserMembershipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserMembership.objects.filter(user=self.request.user).select_related("plan")


class PurchaseMembershipView(APIView):
    """Purchase a membership plan."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        plan_id = request.data.get("plan_id")
        if not plan_id:
            return Response({"detail": "plan_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            plan = MembershipPlan.objects.get(pk=plan_id, is_active=True)
        except MembershipPlan.DoesNotExist:
            return Response({"detail": "Membership plan not found or inactive."}, status=status.HTTP_404_NOT_FOUND)

        # Check if user already has an active membership
        active_membership = UserMembership.objects.filter(
            user=request.user,
            status=UserMembership.STATUS_ACTIVE,
            end_date__gt=timezone.now()
        ).first()

        if active_membership:
            return Response(
                {
                    "detail": "You already have an active membership.",
                    "current_plan": MembershipPlanSerializer(active_membership.plan).data,
                    "expires_at": active_membership.end_date,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create the membership
        start_date = timezone.now()
        end_date = start_date + timedelta(days=plan.duration_days)

        membership = UserMembership.objects.create(
            user=request.user,
            plan=plan,
            start_date=start_date,
            end_date=end_date,
            status=UserMembership.STATUS_ACTIVE,
        )

        # Create a payment record
        Payment.objects.create(
            member=request.user,
            amount=plan.price,
            description=f"Membership: {plan.name}",
            payment_type=Payment.PAYMENT_TYPE_MEMBERSHIP,
        )

        serializer = UserMembershipSerializer(membership)
        return Response(serializer.data, status=status.HTTP_201_CREATED)