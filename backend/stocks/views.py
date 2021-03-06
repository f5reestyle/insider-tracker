from django.db.models import Q, Subquery, Count, Case, When
from django.http import JsonResponse
from django.shortcuts import render
from .models import File, Stock
from .serializers import StockSerializer
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta

# Create your views here.
def latest_filings(request):
    # TODO : 24시간 기준으로 filing 가져온 후, 거기서 Firm ordering.
    today = timezone.now()
    yesterday = today - timedelta(1)

    firm_list = File.objects\
        .filter(Q(created_at__gte=yesterday)|Q(created_at__lte=today))\
        .values('firm_id')\
        .annotate(total=Count('firm_id'))\
        .order_by('-total')\
        .values_list('firm_id',flat=True)
    preserved = Case(*[When(firm_id=firm_id,then=pos) for pos, firm_id in enumerate(firm_list)])
    ticker_list = Stock.objects.filter(firm_id__in=Subquery(firm_list.values('firm_id'))).order_by(preserved)
    data = StockSerializer(ticker_list,many=True).data
    return Response(data)