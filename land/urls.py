from django.urls import path
from .views import LandCreateView, LandDetailView, LandListView, LandTransactionsView

urlpatterns = [
    path('list/', LandListView.as_view(), name='land-list'),  # Public listing
    path('upload/', LandCreateView.as_view(), name='land-upload'),  # Restricted to staff/admin
    path('<int:pk>/', LandDetailView.as_view(), name='land-detail'),  # Restricted detail, edit, delete
    path('<int:land_id>/transactions/', LandTransactionsView.as_view(), name='land_transactions'),
]
