from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Product


class ItemListView(ListView):
    model = Product
    template_name = 'merchstore/item_list.html'


class ItemDetailView(DetailView):
    model = Product
    template_name = 'merchstore/item_detail.html'

def item_list(request):
    items = Product.objects.all() # all objects created through shell
    ctx = {
        "items": items
    }
    return render(request, "merchstore/item_list.html", ctx) 

def item_detail(request, pk):
    ctx = { "item": Product.objects.get(pk=pk) }
    return render(request, 'merchstore/item_detail.html', ctx)
