from django.urls import path
from . import views

app_name = 'currency'
urlpatterns = [
    path('get_exchange_rates/', views.get_exchange_rates),
    path('convert', views.currency_converter), 
]