from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# class Article(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE
#     )
#     title = models.CharField(max_length=100)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=False)
#     updated_at = models.models.DateTimeField(auto_now=False)



class User(AbstractUser):
    def default_product_list():
        return {"deposits": [], "savings": []}
    
    # AbstractUser는 username, email, password를 포함하고 있음!!
    name = models.CharField(max_length=11) # 사용자 이름
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)  # 프로필 이미지
    product_list = models.JSONField(default=default_product_list) 
    
    GENDER_CHOICES = [
        ('male', '남성'),
        ('female', '여성'),
    ]
    MARRIAGE_CHOICES = [
        ('single', '미혼'),
        ('married', '기혼'),
    ]
    INCOME_PROSPECT_CHOICES = [
        ('stable_increase', '안정적 증가'),
        ('unstable', '불안정'),
        ('decreasing', '감소'),
    ]
    ASSET_LEVEL_CHOICES = [
        ('below_10m', '1천만 원 이하'),
        ('10m_to_50m', '1천만~5천만 원'),
        ('50m_to_100m', '5천만~1억 원'),
        ('100m_to_500m', '1억~5억 원'),
        ('500m_to_1b', '5억~10억 원'),
        ('above_1b', '10억 원 이상'),
    ]
    INCOME_LEVEL_CHOICES = [
        ('below_30m', '3천만 원 이하'),
        ('30m_to_50m', '3천만~5천만 원'),
        ('50m_to_70m', '5천만~7천만 원'),
        ('70m_to_100m', '7천만~1억 원'),
        ('100m_to_300m', '1억~3억 원'),
        ('above_300m', '3억 원 이상'),
    ]
    
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')  # 성별
    marriage = models.CharField(max_length=10, choices=MARRIAGE_CHOICES, default='single')  # 혼인 여부
    income_prospect = models.CharField(max_length=20, choices=INCOME_PROSPECT_CHOICES, default='stable_increase')  # 수입 전망
    asset_level = models.CharField(max_length=20, choices=ASSET_LEVEL_CHOICES, default='below_10m')  # 총 자산 규모
    income_level = models.CharField(max_length=20, choices=INCOME_LEVEL_CHOICES, default='below_30m')  # 연 평균 소득
    
    def add_product(self, product_type, product_id):
        if product_type not in ['deposits', 'savings']:
            raise ValueError("Invalid product type")
        
        if self.product_list is None:
            self.product_list = {}

        if product_type not in self.product_list:
            self.product_list[product_type] = []
        
        if product_id not in self.product_list[product_type]:
            self.product_list[product_type].append(product_id)
            self.save()

    def remove_product(self, product_type, product_id):
        if product_type in self.product_list and product_id in self.product_list[product_type]:
            self.product_list[product_type].remove(product_id)
            self.save()

    def __str__(self):
        return self.username  # 사용자 이름 반환