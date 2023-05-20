from rest_framework.viewsets import ReadOnlyModelViewSet

from shop.models import Category, Product, Article
from shop.serializers import CategoryListSerializer, CategoryDetailSerializer, \
    ProductListSerializer, ProductDetailSerializer, ArticleSerializer

# Derived from ReadOnlyViewSet, to refactor rewriting of get_serializer_class method
class CustomReadOnlyModeViewSet(ReadOnlyModelViewSet):
    def get_serializer_class(self):
        if self.action == 'retrieve':
                return self.detail_serializer_class
        return super().get_serializer_class()

class CategoryViewSet(CustomReadOnlyModeViewSet):
    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer

    def get_queryset(self): # Either redefine queryset class attribute or get_queryset method
        return Category.objects.filter(active=True)

class ProductViewSet(CustomReadOnlyModeViewSet):
    
    serializer_class = ProductListSerializer
    detail_serializer_class = ProductDetailSerializer

    def get_queryset(self):
        # filtering only available products first
        queryset = Product.objects.filter(active=True)

        #geting /product/?**category_id**
        category_id = self.request.GET.get('category_id')
        if category_id is not None:
            # narrowing down previously filtered selection
            queryset = queryset.filter(category_id = category_id)
        return queryset
    
class ArticleViewSet(ReadOnlyModelViewSet):
    
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = Article.objects.filter(active=True)
        product_id = self.request.GET.get('product_id')
        if product_id is not None:
            queryset = queryset.filter(product_id = product_id)
        return queryset