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

    data = {}
    for rate in exchange_rates:
        cur_unit = rate['cur_unit']
        deal_bas_r = float(rate['deal_bas_r'].replace(',', '')) #숫자로 저장하기
        data[cur_unit] = deal_bas_r

    return Response(data)

@api_view(['POST'])
def currency_converter(request):

    amount = float(request.data.get("amount")) # 입력값
    from_currency = request.data.get("from_currency") 
    to_currency = request.data.get("to_currency")
    
    exchange_rates = get_exchange_rates(request).data

    if from_currency == 'KRW':
        result = amount / exchange_rates[to_currency]
    elif to_currency == 'KRW':
        result = amount * exchange_rates[from_currency]
    else:
        result = (amount * exchange_rates[from_currency]) / exchange_rates[to_currency]


    return Response({'result': round(result, 2)})

    
