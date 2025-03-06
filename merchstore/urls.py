# merchstore /urls.py
from django.urls import path
from .views import ItemDetailView, ItemListView

urlpatterns = [
    path('items', ItemListView.as_view(), name='item-list'),
    path('item/<int:pk>', ItemDetailView.as_view(), name='item-detail')
]

app_name = "merchstore"
