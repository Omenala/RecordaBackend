from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.utils.html import strip_tags
from .models import Transaction
from .serializers import TransactionSerializer
from datetime import datetime



@api_view(['POST'])
def upload_transaction(request):
    # Check if the user is an admin or has required permissions
    if not request.user.is_staff:
        return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

    # Pass the 'request' context so that the serializer can access the user
    serializer = TransactionSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        # The user is now set by the context in the serializer
        transaction = serializer.save(created_by=request.user)

        # Send a congratulation email if the payment is full, otherwise send receipt
        send_transaction_email(transaction)

         # Here, land is expected as a string, so if you need to do something with it, you can access it:
        #title = serializer.validated_data['land']

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def send_transaction_email(transaction):
    subject = f"Transaction {transaction.transaction_id} - Receipt"
    
    if transaction.payment_method == 'full':
        email_content = f"""
        <p>Dear {transaction.buyer_name},</p>
        <p>Congratulations on your full purchase of the property {transaction.land}, located at {transaction.land.location}!</p>
        <p>Transaction ID: {transaction.transaction_id}</p>
        <p>Total Amount:${transaction.amount}<p>
        <p>Amount Paid: ${transaction.amount_paid}</p>
        <p>Balance: ${transaction.balance}</p>
        <p>Status: {transaction.status}</p>
        <p>Thank you for your purchase!</p>
        """
    else:
        email_content = f"""
        <p>Dear {transaction.buyer_name}</p>
        <p>You just made a part payment for the propert{transaction.land}, located at {transaction.land.location}:<p>
        <p>Transaction ID: {transaction.transaction_id}</p>
        <p>Total Amount:₦{transaction.amount}<p>
        <p>Amount Paid: ₦{transaction.amount_paid}</p>
        <p>Balance: ₦{transaction.balance}</p>
        <p>Status: {transaction.status}</p>
        <p>Thank you for your payment!</p>
        """

    # Send email to the buyer
    send_mail(
        subject,
        strip_tags(email_content),  # Plain text version of the email
        'akubuezehousingestate.info@gmail.com',  # From email
        [transaction.buyer_email],  # To email (buyer)
        html_message=email_content  # HTML version
    )


@api_view(['GET'])
def list_transactions(request):
    """
    List transactions:
    - Admin/staff can see all transactions.
    - Regular users see only their transactions.
    """
    if not request.user.is_authenticated:
        return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

    # If user is staff/admin, show all transactions
    if request.user.is_staff:
        transactions = Transaction.objects.all()
    else:
        # Otherwise, only show transactions created by the user
        transactions = Transaction.objects.filter(user=request.user)

    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def transaction_receipt(request, transaction_id):
    try:
        transaction = Transaction.objects.get(transaction_id=transaction_id)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)
    except Transaction.DoesNotExist:
        return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
def land_transaction_history(request, land_id):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Fetch transactions for the given land_id
    transactions = Transaction.objects.filter(land_id=land_id)
    
    if transactions.exists():
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"error": "No transactions found for this land."}, status=status.HTTP_404_NOT_FOUND)
