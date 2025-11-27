from django.urls import path
from .views import  MemberMembershipPaymentView

urlpatterns = [
    path('membership/', MemberMembershipPaymentView.as_view(), name='member-membership-payment-create'),
]
