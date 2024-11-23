from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.conf import settings
import requests

# Create your views here.
@api_view(['GET'])
def get_exchange_rates(request):
    url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON'
    params = {
        "authkey": settings.CURRENCY_API_KEY,
        "searchdate": "20241122",
        "data": "AP01"
    }
    response = requests.get(url, params=params)
    exchange_rates = response.json()

    data = []
    for rate in exchange_rates:
        currency_info = {
            'cur_unit': rate['cur_unit'],
            'cur_nm': rate['cur_nm'],
            'deal_bas_r': float(rate['deal_bas_r'].replace(',', ''))
        }
        data.append(currency_info)

    return Response(data)
