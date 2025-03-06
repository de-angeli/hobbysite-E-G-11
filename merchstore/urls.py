# merchstore /urls.py
from django.urls import path
from .views import index, ItemDetailView, ItemListView

urlpatterns = [
    path('', index, name='index'),
    path('items', ItemListView.as_view(), name='item-list'),
    path('item/<int:pk>', ItemDetailView.as_view(), name='item-detail')
]
# This might be needed, depending on your Django version
app_name = "merchstore"