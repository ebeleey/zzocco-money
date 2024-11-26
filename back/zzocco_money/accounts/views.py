from django.shortcuts import render
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
import os
import json
import pandas as pd
from django.conf import settings
from .serializers import UserSerializer
from .models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

# Create your views here.

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "회원가입이 완료되었습니다!",
            "user": serializer.data},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user=authenticate(username=username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'key': token.key})
    return Response({'error':'로그인 실패'}, status=400)


# 유저 정보 보내기
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    serializer = UserSerializer(request.user)
    print(serializer.data)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def manage_product(request):
    user = request.user
    action = request.data.get('action')
    product_type = request.data.get('product_type')
    product_id = request.data.get('product_id')

    if action not in ['add', 'remove'] or product_type not in ['deposits', 'savings']:
        return Response({'error': 'Invalid action or product type'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        if action == 'add':
            user.add_product(product_type, product_id)
            message = 'Product added successfully'
        else:  # remove
            user.remove_product(product_type, product_id)
            message = 'Product removed successfully'
        
        return Response({'message': message}, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

# BASE_DIR을 기준으로 파일 경로 설정
csv_file_path = os.path.join(settings.BASE_DIR, 'accounts', 'dummy_user_data_corrected.csv')

def save_users_from_csv():
    # CSV 파일을 pandas DataFrame으로 읽기
    df = pd.read_csv(csv_file_path)
    
    # DataFrame을 JSON 형식으로 변환
    json_data = df.to_dict(orient='records')
    
    for item in json_data:
        # product_list가 JSON 문자열로 되어 있을 경우 변환
        if 'product_list' in item:
            if isinstance(item['product_list'], str):
                try:
                    # JSON 문자열을 Python 딕셔너리로 변환
                    item['product_list'] = json.loads(item['product_list'])
                except json.JSONDecodeError as e:
                    print(f"Invalid JSON in product_list: {item['product_list']}")
                    continue  # 유효하지 않은 JSON 데이터를 건너뜀
            elif not isinstance(item['product_list'], dict):
                print(f"Unexpected type for product_list: {type(item['product_list'])}")
                continue

        # User 모델에 데이터 저장
        if not User.objects.filter(username=item['username']).exists():
            serializer = UserSerializer(data=item)
            
            if serializer.is_valid():
                serializer.save()  # 유효한 경우 데이터베이스에 저장
            else:
                print(serializer.errors)  # 유효하지 않은 경우 오류 출력

@csrf_exempt
def upload_csv(request):
    if request.method == 'POST':
        # CSV 파일로부터 사용자 저장
        save_users_from_csv()
        
        return HttpResponse("CSV file has been processed and users stored in the database.")
    
    return HttpResponse("Please use POST method to upload the CSV.")