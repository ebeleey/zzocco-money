from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.article_list),  # 게시판
    path('<int:article_pk>/', views.article_detail),  # 게시글 페이지
    path('<int:article_pk>/comments/', views.comment_list),
    path('<int:article_pk>/comments/create/', views.comment_create),
    path('comments/<int:comment_pk>/', views.comment_detail),
]