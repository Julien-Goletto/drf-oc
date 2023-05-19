from rest_framework.views import APIView
from rest_framework.response import Response

from shop.models import Category, Product, Article
from shop.serializers import CategorySerializer, ProductSerializer, ArticleSerializer

class CategoryAPIView(APIView):
    def get(self, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class ProductAPIView(APIView):
    def get(self, *args, **kwargs):
      return Response (ProductSerializer(Product.objects.all(), many=True).data)
    
class ArticleAPIView(APIView):
    def get(self, *args, **kwargs):
        return Response (ProductSerializer(Article.objects.all(), many=True).data)