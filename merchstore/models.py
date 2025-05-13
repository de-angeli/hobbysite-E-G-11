from django.db import models
from django.urls import reverse
from user_management.models import Profile

from user_management.models import Profile

class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name = "Product Type"
        verbose_name_plural = "Product Types"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('On Sale', 'On Sale'),
        ('Out of Stock', 'Out of Stock'),
    ]

    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.SET_NULL,
        null=True,
        related_name='item_list'
    ) 
    owner = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
    )
    description = models.TextField()
    price = models.DecimalField(
        max_digits=100,
        decimal_places=2
        )
    stock = models.IntegerField(default=100)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Available'
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.stock == 0:
            self.status = 'Out of Stock'
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('merchstore:item-detail', args=[self.pk])


class Transaction(models.Model):
    STATUS_CHOICES = [
        ('On Cart', 'On Cart'),
        ('To Pay', 'To Pay'),
        ('To Ship', 'To Ship'),
        ('To Receive', 'To Receive'),
        ('Delivered', 'Delivered'),
    ]

    buyer = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
    ) 
    amount = models.IntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='On Cart'
    )

    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.product:
            return self.product.name
        return self.id
        
    def get_absolute_url(self):
        return reverse('merchstore:item-detail', args=[self.pk])
