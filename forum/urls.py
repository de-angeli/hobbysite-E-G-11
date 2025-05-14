from django.urls import path
from .views import ThreadListView, ThreadDetailView, ThreadCreateView, ThreadUpdateView

urlpatterns = [
    path('threads', ThreadListView.as_view(), name="thread-list"),
    path('thread/<int:pk>', ThreadDetailView.as_view(), name="thread-detail"),
    path('thread/add', ThreadCreateView.as_view(), name="thread-create"),
    path('thread/<int:pk>/edit', ThreadUpdateView.as_view(), name="thread-update")
]

app_name = 'forum'
