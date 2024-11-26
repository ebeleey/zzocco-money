from django.urls import path
from . import views

app_name = 'savings'
urlpatterns = [
    path('get-deposits/', views.getDeposit, name='get-deposits'),
    path('get-savings/', views.getSaving, name='get-savings'),
    # path('recommend-products/', views.recommend_products),
    path('similar-users/<int:target_user_id>/', views.find_similar_users, name='find_similar_users'),
]