from django.shortcuts import render

# Create your views here.
from calendar import monthrange
from datetime import datetime
from django.db.models import Sum, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from transaction.models import Transaction 
from land.models import Land

class DashboardView(APIView):
    def get(self, request, *args, **kwargs):
        # Get the current date for monthly and annual calculations
        today = datetime.today()
        current_month = today.month
        current_year = today.year

        # Helper function to calculate monthly breakdown for a given query
        def calculate_monthly_breakdown(queryset, field):
            monthly_data = []
            for month in range(1, 13):
                start_date = datetime(current_year, month, 1)
                end_date = datetime(current_year, month, monthrange(current_year, month)[1])
                value = queryset.filter(date__range=(start_date, end_date)).aggregate(Sum(field))[f'{field}__sum'] or 0
                monthly_data.append({'month': month, 'value': value})
            return monthly_data

        # Calculate monthly revenue breakdown
        monthly_revenue = calculate_monthly_breakdown(Transaction.objects.all(), 'amount_paid')

        # Calculate total revenue for the year
        total_revenue_year = Transaction.objects.filter(date__year=current_year).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0

        # Lands sold breakdown (monthly and annual)
        monthly_lands_sold = [
            {
                "month": month,
                "value": Transaction.objects.filter(
                    date__month=month, date__year=current_year, status="completed"
                ).count(),
            }
            for month in range(1, 13)
        ]
        total_lands_sold_year = Transaction.objects.filter(date__year=current_year, status="completed").count()

        # Lands pending breakdown (monthly and annual)
        monthly_lands_pending = [
            {
                "month": month,
                "value": Transaction.objects.filter(
                    date__month=month, date__year=current_year, status="pending"
                ).count(),
            }
            for month in range(1, 13)
        ]
        total_lands_pending_year = Transaction.objects.filter(date__year=current_year, status="pending").count()

        # Calculate available lands (doesn't need breakdown since it's a current snapshot)
        available_lands = Land.objects.filter(status="available").count()

        # Total lands listed (doesn't need breakdown since it's a snapshot)
        total_lands_listed = Land.objects.count()

        # Prepare response data
        dashboard_data = {
            "revenue": {
                "monthly": monthly_revenue,
                "yearly": total_revenue_year,
            },
            "lands_sold": {
                "monthly": monthly_lands_sold,
                "yearly": total_lands_sold_year,
            },
            "lands_pending": {
                "monthly": monthly_lands_pending,
                "yearly": total_lands_pending_year,
            },
            "available_lands": available_lands,
            "total_lands_listed": total_lands_listed,
        }

        return Response(dashboard_data, status=status.HTTP_200_OK)
