from rest_framework import generics
from shop.models import Category
from shop.serializers import CategorySerializer
from rest_framework.pagination import PageNumberPagination
from shop.models import Product
from shop.serializers import ProductSerializer



class CategoryPagination(PageNumberPagination):
    """Пагинация для категорий"""
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class CategoryListView(generics.ListAPIView):
    """Эндпоинт для получения списка категорий с подкатегориями"""
    queryset = Category.objects.prefetch_related("subcategories").order_by("id")
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination


class ProductPagination(PageNumberPagination):
    """Пагинация для продуктов"""
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class ProductListView(generics.ListAPIView):
    """Эндпоинт для получения списка продуктов"""
    queryset = Product.objects.select_related("category", "subcategory").order_by("id")
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
