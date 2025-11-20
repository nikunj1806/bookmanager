from rest_framework import generics, permissions

from .models import User
from .permissions import IsMemberUser
from .serializers import (
    MemberProfileUpdateSerializer,
    MemberRegistrationSerializer,
    UserSerializer,
)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class MemberRegistrationView(generics.CreateAPIView):
    serializer_class = MemberRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class MemberProfileUpdateView(generics.UpdateAPIView):
    serializer_class = MemberProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsMemberUser]

    def get_object(self):
        return self.request.user


