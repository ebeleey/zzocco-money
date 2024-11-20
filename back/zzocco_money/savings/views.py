from django.shortcuts import render
import requests
# # Create your views here.
# def getdata(request):
#     http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={발급받은 인증키}&topFinGrpNo=020000&pageNo=1
from django.conf import settings


def getdata(request):
    api_key = settings.API_KEY
    url = f"http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1"

    response = requests.get(url).json()
    return Response(response)
