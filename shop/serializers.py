from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError
from shop.models import Category, Product, Article


class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'name', 'product', 'description', 'price', 'date_created', 'date_updated']
    
    def validate_price(self, value):
        if value < 1:
            raise ValidationError("The minimum price is 1€.")
        return value

    def validate_product(self, value):
        print('ceci est le produit passé', value)
        if value.active is False:
            raise ValidationError("The associated product must be active")
        return value

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
        fields = ['id', 'name', 'description', 'date_created', 'date_updated']

    def validate_name(self, value):
        if Category.objects.filter(name=value):
            raise ValidationError('This Category already exists.')
        return value
    
    # Checking if Cat name is present in Cat description for better SEO
    def validate(self, data):
        if data['name'] not in data['description']:
            raise ValidationError('The category name must be repeated somehow in the description.')
        return data

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
