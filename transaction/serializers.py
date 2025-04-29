import random
from rest_framework import serializers
from .models import Transaction
from land.serializers import LandSerializer
from land.models import Land

class TransactionSerializer(serializers.ModelSerializer):
    land_id = serializers.PrimaryKeyRelatedField(queryset=Land.objects.all(), write_only=True)
    land = LandSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'land', 'land_id', 'buyer_name', 'buyer_email', 'buyer_phone',
            'amount', 'amount_paid', 'balance', 'status', 'date',
            'time', 'payment_method', 'transaction_id', 'created_by', 'id'
        ]
        read_only_fields = ['transaction_id', 'created_by']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user
        validated_data['transaction_id'] = f"AHE{random.randint(100000, 99999999)}"
        validated_data['land'] = validated_data.pop('land_id')  # map write-only field to FK
        return super().create(validated_data)
