from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from shop.models import Category, Product, Article
from shop.serializers import CategorySerializer, ProductSerializer

class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    def get_queryset(self):
        return Category.objects.all()

class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    def get_queryset(self):
      return Product.objects.all()