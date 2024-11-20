from django.urls import path, include
from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.signup, name='signup'),  # 직접 작성한 회원가입 View
    path('', include('dj_rest_auth.urls')),  # dj_rest_auth 기본 URL
]