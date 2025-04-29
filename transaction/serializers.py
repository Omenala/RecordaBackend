import random
from rest_framework import serializers
from .models import Transaction
from land.serializers import LandSerializer
from land.models import Land

class TransactionSerializer(serializers.ModelSerializer):
    #land_id = serializers.PrimaryKeyRelatedField(queryset=Land.objects.all(),  write_only=True)
    land = LandSerializer()

    class Meta:
        model = Transaction
        fields = [
            'land', 'land_id', 'buyer_name', 'buyer_email', 'buyer_phone',
            'amount', 'amount_paid', 'balance', 'status', 'date',
            'time', 'payment_method', 'transaction_id', 'created_by', 'id'
        ]
        read_only_fields = ['transaction_id']  # These fields are auto-generated

    def create(self, validated_data):
        # Automatically set the 'created_by' field to the authenticated user
        user = self.context['request'].user  # Assuming the user is authenticated
        validated_data['created_by'] = user
        validated_data['transaction_id'] = f"AHE{random.randint(100000, 99999999)}"
        return super().create(validated_data)
