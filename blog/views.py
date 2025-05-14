from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Article, ArticleCategory, Comment
from .forms import ArticleForm, CommentForm
from user_management.models import Profile
from collections import defaultdict

class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'blog/article_list.html'
    context_object_name = 'all_articles'  # Used in get_context_data

    def get_queryset(self):
        # Fetch all articles, no exclusions
        return Article.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the current user's profile
        user_profile = Profile.objects.get(user=self.request.user)

        # Get the user's articles
        user_articles = Article.objects.filter(author=user_profile)

        # Group all articles (including user's and others') by category
        categorized_articles = defaultdict(list)
        for article in context['all_articles']:
            categorized_articles[article.category].append(article)

        # Exclude the user's articles from the "All Other Articles" section
        other_articles = defaultdict(list)
        for category, articles in categorized_articles.items():
            for article in articles:
                if article.author != user_profile:  # Add to "All Other Articles"
                    other_articles[category].append(article)

        # Pass the grouped articles and the user's articles to the template
        context['user_articles'] = user_articles
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
        return redirect('blog:article_detail', pk=article.pk)

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_form.html'

    def form_valid(self, form):
        form.instance.author = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:article_detail', kwargs={'pk': self.object.pk})

class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_form.html'

    def get_success_url(self):
        return reverse_lazy('blog:article_detail', kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != Profile.objects.get(user=request.user):
            return redirect('blog:article_detail', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)
