from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
from django.http import JsonResponse
from .serializers import DepositSerializer, DepositOptionSerializer, SavingSerializer, SavingOptionSerializer
from .models import Deposit, DepositOption, Saving, SavingOption
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.conf import settings


# # Create your views here.
from django.conf import settings

@api_view(['GET'])
def getDeposit(request):
    api_key = settings.API_KEY

    url = f"http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1"

    response = requests.get(url).json()


    for li in response.get('result').get('baseList'):
        fin_co_no = li.get('fin_co_no')
        kor_co_nm = li.get('kor_co_nm')

        fin_prdt_cd = li.get('fin_prdt_cd')
        fin_prdt_nm = li.get('fin_prdt_nm')
        
        join_way = li.get('join_way')
        join_deny = li.get('join_deny')
        join_member = li.get('join_member')
        spcl_cnd = li.get('spcl_cnd')

        max_limit = li.get('max_limit')
        etc_note = li.get('etc_note')
    
        if not Deposit.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
            save_data = {
                'fin_co_no': fin_co_no,
                'fin_prdt_cd': fin_prdt_cd,
                'kor_co_nm': kor_co_nm,
                'fin_prdt_nm': fin_prdt_nm,
                'etc_note': etc_note,
                'max_limit': max_limit,
                'join_deny': join_deny,
                'join_member': join_member,
                'join_way': join_way,
                'spcl_cnd': spcl_cnd,
            }
            
            serializer = DepositSerializer(data=save_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            
    for li in response.get('result').get('optionList'):
        fin_prdt_cd = li.get('fin_prdt_cd')
        deposit_id = get_object_or_404(Deposit, fin_prdt_cd=fin_prdt_cd)
        intr_rate_type = li.get('intr_rate_type')
        intr_rate_type_nm = li.get('intr_rate_type_nm')
        intr_rate = li.get('intr_rate')
        intr_rate2 = li.get('intr_rate2')
        save_trm = li.get('save_trm')
        rsrv_type = li.get('rsrv_type')
        rsrv_type_nm = li.get('rsrv_type_nm')
        
        if not DepositOption.objects.filter(
                                deposit_id=deposit_id,
                                intr_rate_type=intr_rate_type,
                                save_trm=save_trm
                            ).exists():

            save_data = {
                'deposit_id': deposit_id,
                'intr_rate_type': intr_rate_type,
                'intr_rate_type_nm': intr_rate_type_nm,
                'intr_rate': intr_rate,
                'intr_rate2': intr_rate2,
                'save_trm': save_trm,
                'rsrv_type': rsrv_type,
                'rsrv_type_nm': rsrv_type_nm
            }
            serializer = DepositOptionSerializer(data=save_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(deposit_id=deposit_id)

    # # DepositOption을 미리 필터링하거나, 전체를 가져오고자 할 때
    # deposit_options = DepositOption.objects.all()

    # # Deposit 객체를 가져오면서 DepositOption을 미리 가져오기
    # deposits = Deposit.objects.prefetch_related(Prefetch('options', queryset=deposit_options))

    # # Serializer에서 options를 포함한 Deposit 데이터를 반환
    # deposits_serializer = DepositSerializer(deposits, many=True)
    
    # data = {
    #     "deposit": deposits_serializer.data  # Deposit data with nested options
    # }
    
    options = DepositOption.objects.select_related('deposit_id').values(
        'id',
        'deposit_id__fin_co_no',
        'deposit_id__kor_co_nm',
        'deposit_id__fin_prdt_cd',
        'deposit_id__fin_prdt_nm',
        'deposit_id__join_way',
        'deposit_id__join_deny',
        'deposit_id__join_member',
        'deposit_id__spcl_cnd',
        'deposit_id__etc_note',
        'deposit_id__max_limit',
        'intr_rate_type',
        'intr_rate_type_nm',
        'save_trm',
        'intr_rate',
        'intr_rate2',
    )

    return JsonResponse(list(options), safe=False)

    # return Response(data)

@api_view(['GET'])
def getSaving(request):
    api_key = settings.API_KEY
    
    url = f"http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1"

    response = requests.get(url).json()


    for li in response.get('result').get('baseList'):
        fin_co_no = li.get('fin_co_no')
        kor_co_nm = li.get('kor_co_nm')

        fin_prdt_cd = li.get('fin_prdt_cd')
        fin_prdt_nm = li.get('fin_prdt_nm')
        
        join_way = li.get('join_way')
        join_deny = li.get('join_deny')
        join_member = li.get('join_member')
        spcl_cnd = li.get('spcl_cnd')

        max_limit = li.get('max_limit')
        etc_note = li.get('etc_note')


        if not Saving.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():        
            save_data = {
                'fin_co_no': fin_co_no,
                'fin_prdt_cd': fin_prdt_cd,
                'kor_co_nm': kor_co_nm,
                'fin_prdt_nm': fin_prdt_nm,
                'etc_note': etc_note,
                'max_limit': max_limit,
                'join_deny': join_deny,
                'join_member': join_member,
                'join_way': join_way,
                'spcl_cnd': spcl_cnd,
            }
            
            serializer = SavingSerializer(data=save_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            
    for li in response.get('result').get('optionList'):
        fin_prdt_cd = li.get('fin_prdt_cd')
        saving_id = get_object_or_404(Saving, fin_prdt_cd=fin_prdt_cd)
        intr_rate_type = li.get('intr_rate_type')
        intr_rate_type_nm = li.get('intr_rate_type_nm')
        intr_rate = li.get('intr_rate')
        intr_rate2 = li.get('intr_rate2')
        save_trm = li.get('save_trm')
        rsrv_type = li.get('rsrv_type')
        rsrv_type_nm = li.get('rsrv_type_nm')


        if not SavingOption.objects.filter(
                                saving_id=saving_id,
                                intr_rate_type=intr_rate_type,
                                rsrv_type=rsrv_type,
                                save_trm=save_trm
                            ).exists():
        
            save_data = {
                'saving_id': saving_id,
                'intr_rate_type': intr_rate_type,
                'intr_rate_type_nm': intr_rate_type_nm,
                'intr_rate': intr_rate,
                'intr_rate2': intr_rate2,
                'save_trm': save_trm,
                'rsrv_type': rsrv_type,
                'rsrv_type_nm': rsrv_type_nm
            }
            serializer = SavingOptionSerializer(data=save_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(saving_id=saving_id)

    options = SavingOption.objects.select_related('saving_id').values(
        'id',
        'saving_id__fin_co_no',
        'saving_id__fin_prdt_cd',
        'saving_id__kor_co_nm',
        'saving_id__fin_prdt_nm',
        'saving_id__join_way',
        'saving_id__join_deny',
        'saving_id__join_member',
        'saving_id__spcl_cnd',
        'saving_id__etc_note',
        'saving_id__max_limit',
        'intr_rate_type',
        'intr_rate_type_nm',
        'rsrv_type',
        'rsrv_type_nm',
        'save_trm',
        'intr_rate',
        'intr_rate2',
    )

    return JsonResponse(list(options), safe=False)
    
@api_view(['GET'])
def get_single_deposit(request, pk):
    # select_related를 사용하여 관련된 Deposit 데이터를 미리 가져옵니다.
    deposit_option = DepositOption.objects.select_related('deposit_id').get(pk=pk)

    # DepositOption 데이터를 직렬화합니다.
    deposit_option_data = DepositOptionSerializer(deposit_option).data

    # 관련된 Deposit 데이터를 직접 추가합니다.
    deposit_data = {
        'saving_id__fin_co_no': deposit_option.deposit_id.fin_co_no,
        'saving_id__fin_prdt_cd': deposit_option.deposit_id.fin_prdt_cd,
        'saving_id__kor_co_nm': deposit_option.deposit_id.kor_co_nm,
        'saving_id__fin_prdt_nm': deposit_option.deposit_id.fin_prdt_nm,
        'saving_id__join_way': deposit_option.deposit_id.join_way,
        'saving_id__join_deny': deposit_option.deposit_id.join_deny,
        'saving_id__join_member': deposit_option.deposit_id.join_member,
        'saving_id__spcl_cnd': deposit_option.deposit_id.spcl_cnd,
        'saving_id__etc_note': deposit_option.deposit_id.etc_note,
        'saving_id__max_limit': deposit_option.deposit_id.max_limit,
    }

    # 두 데이터를 합칩니다.
    response_data = {**deposit_option_data, **deposit_data}

    return Response(response_data)


@api_view(['GET'])
def get_single_deposit(request, pk):
    # select_related를 사용하여 관련된 Deposit 데이터를 미리 가져옵니다.
    deposit_option = DepositOption.objects.select_related('deposit_id').get(pk=pk)

    # DepositOption 데이터를 직렬화합니다.
    deposit_option_data = DepositOptionSerializer(deposit_option).data

    # 관련된 Deposit 데이터를 직접 추가합니다.
    deposit_data = {
        'deposit_id__fin_co_no': deposit_option.deposit_id.fin_co_no,
        'deposit_id__fin_prdt_cd': deposit_option.deposit_id.fin_prdt_cd,
        'deposit_id__kor_co_nm': deposit_option.deposit_id.kor_co_nm,
        'deposit_id__fin_prdt_nm': deposit_option.deposit_id.fin_prdt_nm,
        'deposit_id__join_way': deposit_option.deposit_id.join_way,
        'deposit_id__join_deny': deposit_option.deposit_id.join_deny,
        'deposit_id__join_member': deposit_option.deposit_id.join_member,
        'deposit_id__spcl_cnd': deposit_option.deposit_id.spcl_cnd,
        'deposit_id__etc_note': deposit_option.deposit_id.etc_note,
        'deposit_id__max_limit': deposit_option.deposit_id.max_limit,
    }

    # 두 데이터를 합칩니다.
    response_data = {**deposit_option_data, **deposit_data}

    return Response(response_data)

@api_view(['GET'])
def get_single_saving(request, pk):
    # select_related를 사용하여 관련된 Deposit 데이터를 미리 가져옵니다.
    saving_option = SavingOption.objects.select_related('saving_id').get(pk=pk)

    # DepositOption 데이터를 직렬화합니다.
    saving_option_data = SavingOptionSerializer(saving_option).data

    # 관련된 Deposit 데이터를 직접 추가합니다.
    saving_data = {
        'saving_id__fin_co_no': saving_option.saving_id.fin_co_no,
        'saving_id__fin_prdt_cd': saving_option.saving_id.fin_prdt_cd,
        'saving_id__kor_co_nm': saving_option.saving_id.kor_co_nm,
        'saving_id__fin_prdt_nm': saving_option.saving_id.fin_prdt_nm,
        'saving_id__join_way': saving_option.saving_id.join_way,
        'saving_id__join_deny': saving_option.saving_id.join_deny,
        'saving_id__join_member': saving_option.saving_id.join_member,
        'saving_id__spcl_cnd': saving_option.saving_id.spcl_cnd,
        'saving_id__etc_note': saving_option.saving_id.etc_note,
        'saving_id__max_limit': saving_option.saving_id.max_limit,
    }

    # 두 데이터를 합칩니다.
    response_data = {**saving_option_data, **saving_data}

    return Response(response_data)