from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, CustomLoginView

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
]

app_name = 'accounts'