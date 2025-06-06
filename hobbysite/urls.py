"""
URL configuration for hobbysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from user_management import views as user_views
from accounts.views import homepage

urlpatterns = [
    path('', homepage, name='home'),

    path('forum/', include('forum.urls', namespace="forum")),
    path('commissions/', include('commissions.urls', namespace="commissions")),
    path('merchstore/', include('merchstore.urls', namespace="merchstore")),
    path('blog/', include('blog.urls', namespace="blog")),
    path('wiki/', include('wiki.urls', namespace="wiki")),

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('profile/', include('user_management.urls', namespace="user_management")),

    path('admin/', admin.site.urls)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
