from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from shop.models import Category, Product, Article
from shop.serializers import CategoryListSerializer, CategoryDetailSerializer, \
    ProductListSerializer, ProductDetailSerializer, ArticleSerializer

# Mixin rewriting get_serializee_class for derived viewsets
class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class:
                return self.detail_serializer_class
        return super().get_serializer_class()

class CategoryViewSet(MultipleSerializerMixin, ReadOnlyModelViewSet):
    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer

    def get_queryset(self): # Either redefine queryset class attribute or get_queryset method
        return Category.objects.filter(active=True)
    
    # Specific action on post method in order to disable categories
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        # Disable the category
        self.get_object().disable()
        return Response()


class ProductViewSet(MultipleSerializerMixin, ReadOnlyModelViewSet):
    
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
    
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()
    
class ArticleViewSet(ReadOnlyModelViewSet):
    
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = Article.objects.filter(active=True)
        product_id = self.request.GET.get('product_id')
        if product_id is not None:
            queryset = queryset.filter(product_id = product_id)
        return queryset