from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

def post_list(request):
    posts = Post.objects.all()
    ctx = {
        "posts" : posts
    }
    return render(request, 'posts_list.html', ctx)

def post_detail(request, pk):
    ctx = {
        "post" : Post.objects.get(pk=pk)
    }
    return render(request, 'post_detail.html', ctx)
