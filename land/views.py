from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Land
from .serializers import LandSerializer
from rest_framework.generics import ListAPIView  
from transaction.serializers import TransactionSerializer
from rest_framework.permissions import IsAuthenticated
from transaction.models import Transaction 
# Create your views here.


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class LandCreateView(generics.CreateAPIView):
    serializer_class = LandSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class LandDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Land.objects.all()
    serializer_class = LandSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        if not (self.request.user.is_staff or serializer.instance.created_by == self.request.user):
            raise PermissionError("You are not allowed to update this land.")
        serializer.save()

    def perform_destroy(self, instance):
        if not (self.request.user.is_staff or instance.created_by == self.request.user):
            raise PermissionError("You are not allowed to delete this land.")
        instance.delete()

class LandListView(generics.ListAPIView):
    serializer_class = LandSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only registered users can access this

    def get_queryset(self):
        return Land.objects.all()  # Everyone who is logged in can see all lands

class LandTransactionsView(ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]  # Optional: Restrict access to authenticated users

    def get_queryset(self):
        land_id = self.kwargs['land_id']  # Get the land_id from URL parameters
        return Transaction.objects.filter(land_id=land_id)

