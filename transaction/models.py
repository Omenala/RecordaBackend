from django.db import models
from django.conf import settings  # Import settings to access AUTH_USER_MODEL
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.apps import apps  # Import apps for lazy model loading


class Transaction(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    land = models.ForeignKey('land.Land', on_delete=models.CASCADE, null=True)
    transaction_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    buyer_name = models.CharField(max_length=255, null=True, blank=True)
    buyer_email = models.EmailField(max_length=255, null=True, blank=True)
    buyer_phone = models.CharField(max_length=20, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], null=True, blank=True)
    date = models.DateField(auto_now_add=True,null=True, blank=True)
    time = models.TimeField(auto_now_add=True,null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=[('full', 'Full Payment'), ('installment', 'Installment')], default='full', null=True, blank=True)

    
    def save(self, *args, **kwargs):
        if self.amount_paid == self.amount:
            self.status = 'completed'
            self.land.status = 'sold'
        elif self.amount_paid > 0 and self.amount_paid < self.amount:
            self.status = 'pending'
            self.land.status = 'pending'
        else:
            self.status = 'failed'

        self.land.save()  # Save the updated land status
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Transaction {self.transaction_id} for {self.buyer_name}"
