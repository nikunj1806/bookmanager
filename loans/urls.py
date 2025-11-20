from django.urls import path

from .views import MemberBorrowBookView, MemberLoanListView, MemberReturnLoanView

urlpatterns = [
    path('create/', MemberBorrowBookView.as_view(), name='member-borrow-book'),
    path('list/', MemberLoanListView.as_view(), name='member-borrow-list'),
    path('return/<int:loan_id>/', MemberReturnLoanView.as_view(), name='member-borrow-return'),
]
