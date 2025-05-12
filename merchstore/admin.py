from django.contrib import admin
from .models import Product, ProductType, Transaction


class ProductTypeAdmin(admin.ModelAdmin):
    model = ProductType
    list_display = ('name', 'description')
    search_fields = ('name',)


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('name', 'product_type', 'owner', 'price', 'stock', 'status')
    list_filter = ('product_type','status','owner')
    search_fields = ('name',)
    fields = ('name', 'product_type', 'owner', 'description', 'price', 'stock', 'status')


class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
    list_display = ('buyer', 'product', 'status', 'amount',)
    fields = ('buyer', 'product', 'status', 'amount')

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Transaction, TransactionAdmin)
