from django.db import models
from django.urls import reverse


class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField() 

    class Meta: #ProductTypes should be sorted by name in ascending order
        ordering = ['name']

    def __str__(self): #returns string representation of model instance
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(
        ProductType, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='item_list'
    ) 
    description = models.TextField() 
    price = models.DecimalField(max_digits=100,decimal_places=2) #could change due to decimal

    class Meta: #Products should be sorted by name in ascending order
        ordering = ['name']

    def __str__(self): #returns string representation of model instance
        return self.name
        
    def get_absolute_url(self): #returns specific URL for viewing current instance
        return reverse('merchstore:item-detail', args=[self.pk])
