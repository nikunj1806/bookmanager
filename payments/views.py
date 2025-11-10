from rest_framework.views import APIView
from rest_framework.response import Response

class PaymentListView(APIView):
    def get(self, request):
        return Response({"message": "Payment list endpoint working!"})
