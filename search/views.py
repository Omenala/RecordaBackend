from django.http import JsonResponse
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from land.models import Land
from transaction.models import Transaction

class GlobalSearchView(APIView):
    """
    A view to perform global search across Land and Transaction models.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Get the query parameter and initialize the response
        query = request.GET.get('q', '').strip()
        response_data = {'results': []}

        if not query:
            return JsonResponse({'error': 'Search query is required.'}, status=400)

        try:
            # Search for lands matching the query, including status
            land_results = Land.objects.filter(
                Q(title__icontains=query) |
                Q(location__icontains=query) |
                Q(status__icontains=query)  # Add status to the query
            )
            land_data = [
                {
                    'type': 'land',
                    'id': land.id,  # Include ID for navigation
                    'title': land.title,
                    'location': land.location,
                    'status': land.status,  # Include status in the response
                }
                for land in land_results
            ]

            # Search for transactions matching the query
            transaction_results = Transaction.objects.filter(
                Q(transaction_id__icontains=query) | Q(buyer_name__icontains=query)
            )
            transaction_data = [
                {
                    'type': 'transaction',
                    'id': transaction.id,  # Include ID for navigation
                    'transaction_id': transaction.transaction_id,
                    'buyer_name': transaction.buyer_name,
                    'amount': str(transaction.amount),  # Convert Decimal to string
                    'status': transaction.status,
                }
                for transaction in transaction_results
            ]

            # Combine all results
            response_data['results'].extend(land_data)
            response_data['results'].extend(transaction_data)

        except Exception as e:
            return JsonResponse({'error': 'An error occurred during the search.', 'details': str(e)}, status=500)

        # Return the response
        return JsonResponse(response_data, safe=False)
