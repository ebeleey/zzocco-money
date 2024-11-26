from django.urls import path, include
from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.signup, name='signup'),  # 직접 작성한 회원가입 View
    path('login/', views.login, name='login'),
    path('user/', views.user_info, name='user_info'),   # 유저 정보 조회 및 수정
    path('', include('dj_rest_auth.urls')),  # dj_rest_auth 기본 URL
    path('manage-product/', views.manage_product, name='manage_product'),
    path("upload-csv/", views.upload_csv),
    path('update-profile-image/', views.update_profile_image, name='update_profile_image')
]