from django.shortcuts import render, redirect, reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Product, ProductType, Transaction
from .forms import ProductForm, TransactionForm

class ItemListView(ListView):
    model = Product
    template_name = 'merchstore/item_list.html'
    context_object_name = 'all_products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            user_products = Product.objects.filter(owner=profile)
            other_products = Product.objects.exclude(owner=profile)
        else:
            user_products = Product.objects.none()
            other_products = Product.objects.all()

        context['user_products'] = user_products
        context['all_products'] = other_products
        return context
    
class CartListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'merchstore/cart_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = self.request.user.profile
        user_cart_products = Transaction.objects.filter(buyer=profile).select_related('product__owner__user').order_by('product__owner__user__username', 'created_on')

        context['user_cart_products'] = user_cart_products
        return context
        
class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'merchstore/transactions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        profile = self.request.user.profile
        transactions = Transaction.objects.filter(product__owner=profile).select_related('buyer__user', 'product').order_by('buyer__user__username', 'created_on')
        context['transactions'] = transactions
        return context

class ItemDetailView(DetailView):
    model = Product
    template_name = 'merchstore/item_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            user_products = Product.objects.filter(owner=profile)
        else:
            user_products = Product.objects.none()  
        context['user_products'] = user_products
        context['form'] = TransactionForm()
        return context
    
    def post(self, request, *args, **kwargs):
        product = self.get_object()  # Get current product
        form = TransactionForm(request.POST, request.FILES)

        if not request.user.is_authenticated:
            return redirect('login')
        
        if form.is_valid():
            quantity = form.cleaned_data.get('amount')

            if quantity <= product.stock:
                product.stock -= quantity
                product.save()
                
                transaction = Transaction()
                transaction.buyer=request.user.profile
                transaction.product=product
                transaction.amount=form.cleaned_data.get('amount')
                transaction.save()  
                
                return redirect('merchstore:cart-list')
            else:
                return self.get(request, *args, **kwargs) #refresh the page

def add_item(request):
    form = ProductForm()

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            p = Product()
            p.name = form.cleaned_data.get('name')
            p.description = form.cleaned_data.get('description')
            p.price = form.cleaned_data.get('price')
            p.stock = form.cleaned_data.get('stock')
            p.product_type = form.cleaned_data.get('product_type')
            p.status = form.cleaned_data.get('status')
            p.owner = request.user.profile

            if int(p.stock) == 0:
                p.status = 'Out of Stock'
            else:
                p.status = 'Available'

            p.save()
            return redirect(reverse('merchstore:item-list'))
        else:
            form = ProductForm()
            
    ctx = {'form': form}

    return render(request, 'merchstore/item_add.html', ctx)

def update_item(request, pk):
    product = Product.objects.get(pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    
    if form.is_valid():
        if int(product.stock) == 0:
                product.status = 'Out of Stock'
        else:
                product.status = 'Available'
        form.save()
        
        product.save()
        return redirect('merchstore:item-detail', pk=product.pk)  # to go back to original
    
    ctx = {'form': form, 
           'product': product}

    return render(request, 'merchstore/item_edit.html', ctx)

#class CartView(LoginRequiredMixin, ListView): model = Transaction
#class TransactionListView(LoginRequiredMixin, ListView): model = Transaction
