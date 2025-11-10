from rest_framework.views import APIView
from rest_framework.response import Response

class LoanListView(APIView):
    def get(self, request):
        return Response({"message": "Loan list endpoint working!"})
