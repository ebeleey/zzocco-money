from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'name',
            'password',
            'gender',
            'marriage',
            'income_prospect',
            'asset_level',
            'income_level',
            'profile_image',
            'product_list'
        ]

        extra_kwargs = {'password': {'write_only': True}}  # 비밀번호는 쓰기 전용

    def create(self, validated_data):
        # 비밀번호를 validated_data에서 추출
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # 비밀번호 암호화
        user.save()
        return user