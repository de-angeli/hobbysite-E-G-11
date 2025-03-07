from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Article

class ArticleListView(ListView):
    model = Article
    template_name = "wiki/article_list.html"  

class ArticleDetailView(DetailView):
    model = Article
    template_name = "wiki/article_detail.html"

def article_list(request):
    articles = Article.objects.all()
    ctx = {
        "articles": articles
    }
    return render(request, 'wiki/article_list.html', ctx)

def article_detail(request, pk):
    ctx = { "article": Article.objects.get(pk=pk) }
    return render(request, 'wiki/article_detail.html', ctx)