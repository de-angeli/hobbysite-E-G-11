from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy

from .models import Article, ArticleCategory, Comment, ArticleImage
from .forms import ArticleForm, CommentForm
from user_management.models import Profile


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'blog/article_list.html'
    context_object_name = 'other_articles'

    def get_queryset(self):
        user_profile = Profile.objects.get(user=self.request.user)
        return Article.objects.exclude(author=user_profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = Profile.objects.get(user=self.request.user)
        context['user_articles'] = Article.objects.filter(author=user_profile)
        
        other_articles = {}
        for category in ArticleCategory.objects.all():
            articles = Article.objects.filter(category=category).exclude(author=user_profile)
            other_articles[category] = articles
        context['other_articles'] = other_articles
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        context['comments'] = Comment.objects.filter(article=article).order_by('-created_on')
        context['related_articles'] = Article.objects.filter(author=article.author).exclude(id=article.id)[:2]

        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()

        if article.author and article.author.user == self.request.user:
            context['is_owner'] = True
        
        context['gallery_images'] = article.gallery_images.all()

        return context

    def post(self, request, *args, **kwargs):
        article = self.get_object()
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = Profile.objects.get(user=request.user)
                comment.article = article
                comment.save()
        return redirect('blog:article-detail', pk=article.pk)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_create.html'

    def form_valid(self, form):
        form.instance.author = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:article-detail', kwargs={'pk': self.object.pk})

class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_update.html'

    def form_valid(self, form):
        response = super().form_valid(form)

        new_image = form.cleaned_data.get('new_gallery_image')
        if new_image:
            ArticleImage.objects.create(article=self.object, image=new_image)

        return response

    def get_success_url(self):
        return reverse_lazy('blog:article-detail', kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        user_profile = getattr(request.user, 'profile', None)
        if obj.author != user_profile:
            return redirect('blog:article-detail', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)
    