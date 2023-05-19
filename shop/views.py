from rest_framework.viewsets import ReadOnlyModelViewSet

from shop.models import Category, Product, Article
from shop.serializers import CategorySerializer, ProductSerializer

class CategoryViewSet(ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    def get_queryset(self):
        return Category.objects.all()

class ProductViewSet(ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    def get_queryset(self):
      return Product.objects.all()