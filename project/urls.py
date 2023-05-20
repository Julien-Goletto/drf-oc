from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from shop.views import CategoryViewSet, ProductViewSet, ArticleViewSet, AdminCategoryViewSet

# Creating a router
router = routers.SimpleRouter()
router.register('category', CategoryViewSet, basename='category')
router.register('product', ProductViewSet, basename='product')
router.register('article', ArticleViewSet, basename='article')
router.register('admin/category', AdminCategoryViewSet, basename='admin-category')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)), # Using router registered routes
]
