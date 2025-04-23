from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Thread, ThreadCategory


class CategoryListView(ListView):
    model = ThreadCategory
    template_name = 'forum/thread_list.html'


class PostDetailView(DetailView):
    model = Thread
    template_name = 'forum/thread_detail.html'

def post_list(request):
    categories = ThreadCategory.objects.prefetch_related('posts')
    posts = Thread.objects.all()
    ctx = {
        "categories": categories,
        "posts" : posts
    }
    return render(request, 'forum/thread_list.html', ctx)

def post_detail(request, pk):
    ctx = { "post" : Thread.objects.get(pk=pk) }
    return render(request, 'forum/thread_detail.html', ctx)
