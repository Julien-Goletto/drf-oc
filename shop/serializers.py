from rest_framework.serializers import ModelSerializer
from shop.models import Category, Product, Article

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'active', 'date_created', 'date_updated']

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'active', 'category_id', 'date_created', 'date_updated']

class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'name', 'description', 'active', 'price', 'product_id', 'date_created', 'date_updated']