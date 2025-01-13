from django.db import models
from django.contrib.auth import get_user_model
from transaction.models import Transaction

# Use the custom user model
User = get_user_model()

class Land(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
    ]

    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    size = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='available')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uploaded_lands", null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    # New field: A ForeignKey to the Transaction model, which will track transactions linked to this land
    transactions = models.ManyToManyField('transaction.Transaction', related_name='land_transactions', blank=True)

    def __str__(self):
        return self.title

    def get_transaction_history(self):
        """Retrieve transactions related to this land based on status."""
        return self.transactions.all()

    def get_pending_transactions(self):
        """Retrieve pending transactions for this land."""
        return self.transactions.filter(status='pending')

    def get_completed_transactions(self):
        """Retrieve completed transactions for this land."""
        return self.transactions.filter(status='completed')
