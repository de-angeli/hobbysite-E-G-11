from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from .models import Profile
from .forms import ProfileForm


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'user_management/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('home')

    def get_object(self):
        username = self.kwargs['username']
        profile = get_object_or_404(Profile, user__username=username)

        if profile.user != self.request.user:
            raise PermissionDenied

        return profile
