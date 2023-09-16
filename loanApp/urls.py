from django.urls import path
from loanApp import views


app_name = 'loanApp'
urlpatterns = [
    path('loan-request/', views.LoanRequest, name='loan_request'),
    path('loan-payment/', views.LoanPayment, name='loan_payment'),
    path('user-transaction/', views.UserTransaction, name='user_transaction'),
    path('user-loan-history/', views.UserLoanHistory, name='user_loan_history'),
    path('user-paid-history/', views.UserLoanPaidHistory, name='user_loan_paid_history'),
    path('user-loan-history-admin/', views.UserLoanHistoryAdmin, name='user_loan_history_admin'),
    path('user-dashboard/', views.UserDashboard, name='user_dashboard'),
    path('loan-details/', views.user_loan_details, name='user_loan_details'),
    path('loan-accept/<int:pk>', views.loan_accept, name='user_loan_accept'),
    path('loan-reject/<int:pk>', views.loan_reject, name='user_loan_accept'),
    path('ssl/status/', views.ssl_status, name='ssl_status'),
    path('ssl/complate/<val_id>/<tran_id>', views.ssl_complate, name='ssl_complate'),

]
