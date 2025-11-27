from django.urls import path
from .views import MemberBuyBookPaymentView, MemberPaymentListView

urlpatterns = [
    path('book/', MemberBuyBookPaymentView.as_view(), name='purchase-book'),
    path('list/', MemberPaymentListView.as_view(), name='purchase-book-list'),
]

