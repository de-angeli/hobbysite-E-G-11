from django.contrib import admin
from .models import Product, ProductType


class ProductTypeAdmin(admin.ModelAdmin):
    model = ProductType
    list_display = ('name', 'description')
    search_fields = ('name',)


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('name', 'product_type', 'price')
    list_filter = ('product_type',)
    search_fields = ('name',)
    fields = ('name', 'product_type', 'description', 'price')

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
