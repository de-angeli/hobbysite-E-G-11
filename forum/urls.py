from django.urls import path
from .views import CategoryListView, PostDetailView

urlpatterns = [
    path('threads', CategoryListView.as_view(), name="thread-list"),
    path('thread/<int:pk>', PostDetailView.as_view(), name="thread-detail")
]

app_name = 'forum'
