from django.urls import path, include
from . import views

app_name = 'savings'
urlpatterns = [
    path('get/', views.getdata, name='getdata'),  # 직접 작성한 회원가입 View
]