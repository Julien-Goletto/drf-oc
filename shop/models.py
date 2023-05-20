from django.db import models
from django.db import transaction
from requests import request
from rest_framework import status

class fetchMixin:
    def call_external_api(self, method, url):
        return request(method, url)

class Category(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    # atomic decorator allows to cancel a transaction if any of its steps fails
    @transaction.atomic
    def disable(self):
        if self.active is False:
            return
        self.active = False
        self.save()
        self.products.update(active=False)

class Product(fetchMixin, models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)

    category = models.ForeignKey('shop.Category', on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name
    
    @transaction.atomic
    def disable(self):
        if self.active == False:
            return
        self.active = False
        self.save()
        self.articles.update(active=False)
    
    # Declaring an additionnal property to
    @property
    def ecoscore(self):
        response = self.call_external_api('GET', 'https://world.openfoodfacts.org/api/v0/product/3229820787015.json')
        if response.status_code == status.HTTP_200_OK:
            return response.json()['product']['ecoscore_grade']


class Article(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return self.name
