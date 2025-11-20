from django.urls import path
from .views import MemberPaymentListView, MemberMembershipPaymentView, MemberBuyBookPaymentView
urlpatterns = [
    path('list/', MemberPaymentListView.as_view(), name='member-payment-list'),
    path('membership/', MemberMembershipPaymentView.as_view(), name='member-membership-payment-create'),
    path('buy/book/', MemberBuyBookPaymentView.as_view(), name='member-buy-payment'),
]
