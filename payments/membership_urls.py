from django.urls import path
from .views import (
    MembershipPlanListView,
    UserMembershipListView,
    PurchaseMembershipView,
)

urlpatterns = [
    path('plans/', MembershipPlanListView.as_view(), name='membership-plan-list'),
    path('my/', UserMembershipListView.as_view(), name='user-membership-list'),
    path('purchase/', PurchaseMembershipView.as_view(), name='purchase-membership'),
]

