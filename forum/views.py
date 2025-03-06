from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Post, PostCategory


class CategoryListView(ListView):
    model = PostCategory
    template_name = 'forum/thread_list.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'forum/thread_detail.html'

def post_list(request):
    categories = PostCategory.objects.prefetch_related('posts')
    posts = Post.objects.all()
    ctx = {
        "categories": categories,
        "posts" : posts
    }
    return render(request, 'forum/thread_list.html', ctx)

def post_detail(request, pk):
    ctx = { "post" : Post.objects.get(pk=pk) }
    return render(request, 'forum/thread_detail.html', ctx)
