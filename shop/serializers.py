from rest_framework.serializers import ModelSerializer, SerializerMethodField
from shop.models import Category, Product, Article


class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'name', 'description', 'active', 'price', 'product_id', 'date_created', 'date_updated']

class ProductListSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'date_created', 'date_updated']

class ProductDetailSerializer(ModelSerializer):
    articles = SerializerMethodField()
    def get_articles(self, instance):
        queryset = instance.articles.filter(active=True)
        return ArticleSerializer(queryset, many=True).data

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'active', 'category_id', 'articles', 'date_created', 'date_updated']

class CategoryListSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'date_created', 'date_updated']

class CategoryDetailSerializer(ModelSerializer):
    """ Defining product attribute by coupling with its own serializer
        Using SerializerMethodField allow to perform extra modifications (sorting, filtering...)
        But needs a specific get_object method addition"""
    products = SerializerMethodField()
    def get_products(self, instance):
        # instance refers to the current category, involving recursivity for each available category
        queryset = instance.products.filter(active=True)
        return ProductDetailSerializer(queryset, many=True).data
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'products', 'date_created', 'date_updated']
