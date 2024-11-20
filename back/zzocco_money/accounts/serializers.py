from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    gender = serializers.ChoiceField(choices=User.GENDER_CHOICES)  # 성별
    marriage = serializers.ChoiceField(choices=User.MARRIAGE_CHOICES)  # 혼인 여부
    income_prospect = serializers.ChoiceField(choices=User.INCOME_PROSPECT_CHOICES)  # 수입 전망
    asset_level = serializers.ChoiceField(choices=User.ASSET_LEVEL_CHOICES)  # 총 자산 규모
    income_level = serializers.ChoiceField(choices=User.INCOME_LEVEL_CHOICES)  # 연 평균 소득

    class Meta:
        model = User
        fields = [
            'id',              # Django 기본 ID
            'username',        # 사용자 이름
            'email',           # 이메일
            'profile_image',   # 프로필 이미지 URL
            'product_list',    # 제품 목록 (JSON 형태)
            'gender',          # 성별
            'marriage',        # 혼인 여부
            'income_prospect', # 수입 전망
            'asset_level',     # 총 자산 규모
            'income_level',    # 연 평균 소득
        ]
        read_only_fields = ['id']  # 읽기 전용 필드

    def validate(self, data):
    if data['password1'] != data['password2']:
        raise serializers.ValidationError({"password2": "Passwords do not match."})
    return data

    def create(self, validated_data):
        validated_data.pop('password2')  # password2는 저장하지 않음
        password = validated_data.pop('password1')
        user = User(**validated_data)
        user.set_password(password)  # 비밀번호 암호화
        user.save()
        return user