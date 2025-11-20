from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Loan
from .serializers import LoanSerializer, BorrowRequestSerializer
from .services import create_membership_loan, LoanUnavailableError, return_loan

from users.permissions import IsMemberUser
from rest_framework import permissions

class MemberBorrowBookView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsMemberUser]

    def post(self, request):
        payload = request.data  
        payload["member_id"] = request.user.id
        serializer = BorrowRequestSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        due_date = serializer.validated_data["due_date"]
        inventory = serializer.validated_data["inventory"]
        member = serializer.validated_data["member"]
        try:
            loan = create_membership_loan(member, inventory, due_date)
        except LoanUnavailableError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(LoanSerializer(loan).data, status=status.HTTP_201_CREATED)

class MemberLoanListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsMemberUser]
    serializer_class = LoanSerializer

    def get_queryset(self):
        member_id = self.request.user.id
        queryset = (
            Loan.objects.filter(member_id=member_id)
            .select_related("member", "book", "store", "store_inventory")
            .order_by("-loan_date")
        )
        return queryset

class MemberReturnLoanView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsMemberUser]

    def post(self, request, loan_id):
        try:
            loan = Loan.objects.get(pk=loan_id, member=request.user)
        except Loan.DoesNotExist:
            return Response({"detail": "Loan not found."}, status=status.HTTP_404_NOT_FOUND)

        if loan.status == Loan.STATUS_RETURNED:
            return Response({"detail": "Loan already returned."}, status=status.HTTP_400_BAD_REQUEST)

        loan = return_loan(loan)
        return Response(LoanSerializer(loan).data, status=status.HTTP_200_OK)  