from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .forms import LoanRequestForm, LoanTransactionForm
from .models import loanRequest, loanTransaction, CustomerLoan
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.db.models import Sum
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal


def home(request):
    return render(request, 'home.html', context={})


@login_required(login_url='/account/login-customer')
def LoanRequest(request):
    form = LoanRequestForm()

    if request.method == 'POST':
        form = LoanRequestForm(request.POST)

        if form.is_valid():
            loan_obj = form.save(commit=False)
            loan_obj.customer = request.user.customer
            total_amount = loan_obj.amount
            loan_year = loan_obj.year
            total_cal = (total_amount / 100) * 9
            total_cal += total_amount
            if loan_year == 2:
                total_cal += 1000
            elif loan_year == 3:
                total_cal += 3000
            loan_obj.amount = total_cal
            loan_obj.save()
            return redirect('/')

    return render(request, 'loanApp/loanrequest.html', context={'form': form})


@login_required(login_url='/account/login-customer')
def LoanPayment(request):
    form = LoanTransactionForm()
    store_id = settings.STORE_ID
    store_pass = settings.STORE_PASS

    if request.method == 'POST':
        mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id,
                                sslc_store_pass=store_pass)
        status_url = request.build_absolute_uri('/loan/ssl/status/')
        mypayment.set_urls(success_url=status_url, fail_url='/',
                           cancel_url='/')
        mypayment.set_product_integration(total_amount=int(request.POST.get('payment')), currency='BDT', product_category='clothing',
                                          product_name='demo-product', num_of_item=2, shipping_method='YES',
                                          product_profile='None')
        mypayment.set_customer_info(name='John Doe', email='johndoe@email.com', address1='demo address',
                                    address2='demo address 2', city='Dhaka', postcode='1207', country='Bangladesh',
                                    phone='01711111111')
        mypayment.set_shipping_info(shipping_to='demo customer', address='demo address', city='Dhaka', postcode='1209',
                                    country='Bangladesh')

        mypayment.set_additional_values(value_a='cusotmer@email.com', value_b='portalcustomerid', value_c='1234',
                                        value_d='uuid')

        response_data = mypayment.init_payment()
        form = LoanTransactionForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.customer = request.user.customer
            payment.save()

        return redirect(response_data['GatewayPageURL'])

        # form = LoanTransactionForm(request.POST)
        # if form.is_valid():
        #     payment = form.save(commit=False)
        #     payment.customer = request.user.customer
        #     payment.save()
        #     # pay_save = loanTransaction()
        #     return redirect('/')

    return render(request, 'loanApp/payment.html', context={'form': form})

@csrf_exempt
def ssl_status(request):
    return redirect('/')


def ssl_complate(request, pk, id):
    return HttpResponse('hello')


@login_required(login_url='/account/login-customer')
def UserTransaction(request):
    transactions = loanTransaction.objects.filter(
        customer=request.user.customer)
    return render(request, 'loanApp/user_transaction.html', context={'transactions': transactions})


@login_required(login_url='/account/login-customer')
def UserLoanHistory(request):
    loans = loanRequest.objects.filter(
        customer=request.user.customer)
    return render(request, 'loanApp/user_loan_history.html', context={'loans': loans})


@login_required(login_url='/account/login-customer')
def UserLoanPaidHistory(request):
    loans = loanTransaction.objects.filter(
        customer=request.user.customer)
    return render(request, 'loanApp/user_loan_paid_history.html', context={'loans': loans})


def UserLoanHistoryAdmin(request):
    loans = loanRequest.objects.all()
    return render(request, 'loanApp/user_loan_history.html', context={'loans': loans})


@login_required(login_url='/account/login-customer')
def UserDashboard(request):
    requestLoan = loanRequest.objects.all().filter(
        customer=request.user.customer).count(),
    approved = loanRequest.objects.all().filter(
        customer=request.user.customer).filter(status='accept').count(),
    rejected = loanRequest.objects.all().filter(
        customer=request.user.customer).filter(status='reject').count(),
    # totalLoan = CustomerLoan.objects.filter(customer=request.user.customer).aggregate(Sum('total_loan'))[
    #     'total_loan__sum'],
    # totalPayable = CustomerLoan.objects.filter(customer=request.user.customer).aggregate(
    #     Sum('payable_loan'))['payable_loan__sum'],
    # totalPaid = loanTransaction.objects.filter(customer=request.user.customer).aggregate(Sum('payment'))[
    #     'payment__sum'],

    total_loan_amount = 0
    totalPayable = 0
    totalPaid = 0
    total_year = 0
    approve_loan_amount = loanRequest.objects.all()
    for data in approve_loan_amount:
        if data.status == 'accept' and data.customer == request.user.customer:
            total_loan_amount += data.amount
            if total_year < data.year:
                total_year = data.year
    if total_loan_amount > 0:
        totalPayable = total_loan_amount // (total_year*12)

    totalPaidObj = loanTransaction.objects.all()
    for data in totalPaidObj:
        if data.customer == request.user.customer:
            totalPaid += data.payment
    due_loan = total_loan_amount - totalPaid
    data_dict = {
        'request': requestLoan[0],
        'approved': approved[0],
        'rejected': rejected[0],
        'totalLoan': total_loan_amount,
        'totalPayable': totalPayable,
        'totalPaid': totalPaid,
        'due_loan': due_loan,

    }

    return render(request, 'loanApp/user_dashboard.html', context=data_dict)


from django.shortcuts import render
from .models import CustomerSignUp, CustomerLoan, loanTransaction


def user_loan_details(request):
    user = request.user  # Assuming you're using Django's built-in User model
    customer = CustomerSignUp.objects.get(user=user)
    loans = CustomerLoan.objects.filter(customer=customer)
    transactions = loanTransaction.objects.filter(customer=customer)

    context = {
        'customer': customer,
        'loans': loans,
        'transactions': transactions,
    }
    return render(request, 'loan_details.html', context)


def error_404_view(request, exception):
    print("not found")
    return render(request, 'notFound.html')


def loan_accept(request, pk):
    obj = loanRequest.objects.get(id=pk)
    obj.status = 'accept'
    obj.save()

    return redirect("/loan/user-loan-history-admin/")


def loan_reject(request, pk):
    obj = loanRequest.objects.get(id=pk)
    obj.status = 'reject'
    obj.save()

    return redirect("/loan/user-loan-history-admin/")
