from django.urls import path
from .views import CategoryListView, PostDetailView

urlpatterns = [
    path('forum/threads', CategoryListView.as_view(), name="thread-list"),
    path('forum/thread/<int:pk>', PostDetailView.as_view(), name="thread-detail")
]

app_name = 'forum'
