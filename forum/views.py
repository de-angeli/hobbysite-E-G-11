from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Thread, ThreadCategory
from .forms import ThreadForm, CommentForm


class ThreadListView(ListView):
    model = Thread
    template_name = 'forum/thread_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = ThreadCategory.objects.prefetch_related('posts')

        user = self.request.user

        if self.request.user.is_authenticated:
            ctx['user_threads'] = Thread.objects.filter(author=user.profile)
            # exclude user's threads from the main categories
            for category in ctx['categories']:
                category.filtered_posts = category.posts.exclude(author=user.profile)
        else:
            for category in ctx['categories']:
                category.filtered_posts = category.posts.all()
        return ctx


class ThreadDetailView(DetailView):
    model = Thread
    template_name = 'forum/thread_detail.html'

    def get_success_url(self):
        return reverse('forum:thread-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            ctx['form'] = CommentForm()

        ctx['comments'] = self. object.comment.order_by('created_on')
        ctx['related_posts'] = Thread.objects.filter(
            category=self.object.category
        ).exclude(pk=self.object.pk)[:2]
        ctx['categories'] = ThreadCategory.objects.prefetch_related('posts')

        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = self.object
            comment.author = request.user.profile
            comment.save()
            return redirect(self.get_success_url())
        else:
            ctx = self.get_context_data()
            ctx['form'] = form
            return self.render_to_response(ctx)


class ThreadCreateView(LoginRequiredMixin, CreateView):
    model = Thread
    template_name = 'forum/thread_create.html'
    form_class = ThreadForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form = ThreadForm(request.POST, request.FILES)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = self.request.user.profile
            thread.save()
            return redirect(self.get_success_url())
        else:
            return render(request, self.template_name, {'form': form})

    def get_success_url(self):
        return reverse('forum:thread-list')


class ThreadUpdateView(LoginRequiredMixin, UpdateView):
    model = Thread
    template_name = 'forum/thread_update.html'
    form_class = ThreadForm

    def get_queryset(self):
        return Thread.objects.filter(author=self.request.user.profile)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, request.FILES, instance=self.object)

        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = self.request.user.profile
            thread.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('forum:thread-detail', kwargs={'pk': self.object.pk})
