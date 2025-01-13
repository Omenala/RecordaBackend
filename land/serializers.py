from rest_framework import serializers
from .models import Land

class LandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Land
        fields = ['id', 'title', 'location', 'size', 'price', 'status', 'created_by', 'created_at']
