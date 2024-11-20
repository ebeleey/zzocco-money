from django.urls import path
from . import views

app_name = 'savings'
urlpatterns = [
    path('get-deposits/', views.getDeposit, name='get-deposits'),
    path('get-savings/', views.getSaving, name='get-savings'),
]