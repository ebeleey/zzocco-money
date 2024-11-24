from django.shortcuts import render
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token


from .models import User
from .serializers import UserSerializer

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