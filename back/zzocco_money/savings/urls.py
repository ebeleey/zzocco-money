from django.urls import path
from . import views

app_name = 'savings'
urlpatterns = [
    path('get-deposits/', views.getDeposit, name='get-deposits'),
    path('get-savings/', views.getSaving, name='get-savings'),
    path('similar-users/<int:target_user_id>/', views.find_similar_users, name='find_similar_users'),
    path('get-single-deposit/<int:pk>/', views.get_single_deposit, name='get-single-deposit'),
    path('get-single-saving/<int:pk>/', views.get_single_saving, name='get-single-saving')
]