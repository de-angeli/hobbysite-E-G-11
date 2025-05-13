from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Article, ArticleCategory
from .forms import CommentForm, ArticleForm


class ArticleListView(ListView):
    model         = Article
    template_name = 'wiki/article_list.html'

    def get_context_data(self, **kwargs):
        ctx  = super().get_context_data(**kwargs)
        user = self.request.user

        profile = getattr(user, 'profile', None) if user.is_authenticated else None

        your_qs  = Article.objects.filter(author=profile).order_by('-created_on') if profile else Article.objects.none()
        other_qs = Article.objects.exclude(author=profile).order_by('-created_on') if profile else Article.objects.all().order_by('-created_on')

        cats = ArticleCategory.objects.filter(articles__in=other_qs).distinct().order_by('name')
        grouped = {cat: other_qs.filter(category=cat) for cat in cats}

        ctx.update({
            'your_articles':              your_qs,
            'all_articles_by_category':   grouped,
        })
        return ctx


class ArticleDetailView(DetailView):
    model         = Article
    template_name = 'wiki/article_detail.html'

    def get_context_data(self, **kwargs):
        ctx     = super().get_context_data(**kwargs)
        article = self.object

        ctx['read_more']    = (
            Article.objects
                   .filter(category=article.category)
                   .exclude(pk=article.pk)[:2]
        )

        ctx['comments']     = article.comments.all().order_by('-created_on')
        ctx['comment_form'] = CommentForm()
        return ctx

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment         = comment_form.save(commit=False)
            comment.author  = request.user.profile
            comment.article = self.get_object()
            comment.save()
        return redirect(self.get_object().get_absolute_url())


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model         = Article
    form_class    = ArticleForm
    template_name = 'wiki/article_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model         = Article
    form_class    = ArticleForm
    template_name = 'wiki/article_form.html'

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user.profile)
