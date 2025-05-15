from django.urls import path
from .views import ItemDetailView, ItemListView, CartListView, TransactionListView, add_item, update_item

urlpatterns = [
    path('items/', ItemListView.as_view(), name='item-list'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('item/add/', add_item, name='item-add'),
    path('item/<int:pk>/edit/', update_item, name='item-edit'),
    path('cart/', CartListView.as_view(), name='cart-list'),
    path('transactions/', TransactionListView.as_view(), name='transaction-list')    
]

app_name = "merchstore"
