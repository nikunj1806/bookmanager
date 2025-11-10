from rest_framework import generics
from .models import User
from .serializers import UserSerializer

# ✅ List all users OR create new user
class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# ✅ Retrieve, update or delete a specific user
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
