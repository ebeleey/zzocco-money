from django.db import models

# Create your models here.

class Deposit(models.Model):
    fin_co_no = models.TextField(null=False)     # 금융 회사 코드
    kor_co_nm = models.TextField(null=False)    # 금융회사 명

    fin_prdt_cd = models.TextField(unique=True)   # 금융 상품 코드
    fin_prdt_nm = models.TextField(null=False)   # 금융상품명
    
    join_way = models.TextField(null=False)   # 가입방법
    join_deny = models.IntegerField(null=False, choices=[(1, "제한없음"), (2, "서민전용"), (3, "일부제한")])
    join_member = models.TextField(null=False)  # 가입 대상
    spcl_cnd = models.TextField(null=False)    # 우대조건
    
    etc_note = models.TextField(null=True, blank=True)
    max_limit = models.BigIntegerField(null=True, blank=True)


class DepositOption(models.Model):
    deposit_id = models.ForeignKey(Deposit, related_name='options', on_delete=models.CASCADE)   # FK: 어느 상품의 옵션인지
    intr_rate_type = models.CharField(max_length=10)    # 저축 금리 유형
    intr_rate_type_nm = models.CharField(max_length=100)    # 저축 금리 유형명
    save_trm = models.IntegerField()    # 저축 기간
    intr_rate = models.DecimalField(max_digits=5, decimal_places=2)     # 저축 금리(소수점 2자리)
    intr_rate2 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)     # 최고 우대 금리(소수점 2자리)


class Saving(models.Model):
    fin_co_no = models.TextField(null=False)     # 금융 회사 코드
    kor_co_nm = models.TextField(null=False)    # 금융회사 명

    fin_prdt_cd = models.TextField(unique=True)   # 금융 상품 코드
    fin_prdt_nm = models.TextField(null=False)   # 금융상품명
    
    join_way = models.TextField(null=False)   # 가입방법
    join_deny = models.IntegerField(null=False, choices=[(1, "제한없음"), (2, "서민전용"), (3, "일부제한")])
    join_member = models.TextField(null=False)  # 가입 대상
    spcl_cnd = models.TextField(null=False)    # 우대조건
    
    etc_note = models.TextField(null=True, blank=True)
    max_limit = models.BigIntegerField(null=True, blank=True)


class SavingOption(models.Model):
    saving_id = models.ForeignKey(Saving, on_delete=models.CASCADE)   # FK: 어느 상품의 옵션인지
    intr_rate_type = models.CharField(max_length=10)    # 저축 금리 유형
    intr_rate_type_nm = models.CharField(max_length=100)    # 저축 금리 유형명
    rsrv_type = models.CharField(null=True, max_length=10)     # 적립 유형
    rsrv_type_nm = models.CharField(null=True, max_length=50)  # 적립 유형명
    save_trm = models.IntegerField()    # 저축 기간
    intr_rate = models.DecimalField(max_digits=5, decimal_places=2)     # 저축 금리(소수점 2자리)
    intr_rate2 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)     # 최고 우대 금리(소수점 2자리)