from django.db import models
from django.contrib.auth.models import User
from loginApp.models import CustomerSignUp
import uuid
# Create your models here.


class loanCategory(models.Model):
    loan_name = models.CharField(max_length=250)
    creation_date = models.DateField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.loan_name


class loanParcent(models.Model):
    loan_parc = models.IntegerField(blank=True, null=True)

    def __str__(self):
        loan_parc = str(self.loan_parc)
        return loan_parc




class loanRequest(models.Model):
    CHOICES = (
        ("pending", "Pending"),
        ("reject", "Reject"),
        ("accept", "Accepted"),
    )

    customer = models.ForeignKey(
        CustomerSignUp, on_delete=models.CASCADE, related_name='loan_customer')

    loanParcent = models.ForeignKey(
        loanParcent, on_delete=models.CASCADE, related_name='loan_parcent', blank=True, null=True)

    category = models.ForeignKey(
        loanCategory, on_delete=models.CASCADE, null=True)
    request_date = models.DateField(auto_now_add=True)
    status_date = models.CharField(
        max_length=150, null=True, blank=True, default=None)
    reason = models.TextField()
    status = models.CharField(default='pending', max_length=10, choices=CHOICES, blank=True, null=True)
    amount = models.PositiveIntegerField(default=0)
    year = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f" {self.customer.user.username} ---- {self.status}"


class CustomerLoan(models.Model):
    customer = models.ForeignKey(
        CustomerSignUp, on_delete=models.CASCADE, related_name='loan_user')
    total_loan = models.PositiveIntegerField(default=0)
    payable_loan = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.customer.user.username


class loanTransaction(models.Model):
    customer = models.ForeignKey(
        CustomerSignUp, on_delete=models.CASCADE, related_name='transaction_customer')

    transaction = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    payment = models.PositiveIntegerField(default=0)
    payment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.customer.user.username
