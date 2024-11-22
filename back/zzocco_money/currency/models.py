from django.db import models

# Create your models here.
class ExchangeRate(models.Model):
    cur_unit = models.CharField(max_length=10)  # 통화코드
    cur_nm = models.CharField(max_length=50)    # 국가/통화명
    deal_bas_r = models.FloatField()            # 매매기준율