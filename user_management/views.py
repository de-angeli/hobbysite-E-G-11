from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Profile
from .forms import ProfileForm

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    ctx = {
        "form" : form
    }
    return render(request, 'registration/register.html', ctx)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'user_management/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('home')

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
