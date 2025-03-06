from django.urls import path
from .views import article_list, article_detail

app_name = 'blog'

urlpatterns = [
    path('articles/', article_list, name='article_list'),
    path('article/<int:article_id>/', article_detail, name='article_detail'),
]
