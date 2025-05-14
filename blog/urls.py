from django.urls import path
from django.views.generic.base import RedirectView
from .views import ArticleListView, ArticleDetailView, ArticleCreateView, ArticleUpdateView

app_name = 'blog'

urlpatterns = [
    path('', RedirectView.as_view(url='/blog/articles/', permanent=False)),  # Redirect from /blog/ to /blog/articles/
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('article/add/', ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('article/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_update'),
]
