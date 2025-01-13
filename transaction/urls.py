from django.urls import path
from . import views
from .views import land_transaction_history

urlpatterns = [
    path('upload/', views.upload_transaction, name='upload_transaction'),
    path('list-transactions/', views.list_transactions, name='list_transactions'),
    path('<str:transaction_id>/', views.transaction_receipt, name='transaction_receipt'),
     path('land/<int:land_id>/transactions/', land_transaction_history, name='land-transactions'),

]