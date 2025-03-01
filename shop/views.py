from rest_framework import generics
from shop.models import Category
from shop.serializers import CategorySerializer
from rest_framework.pagination import PageNumberPagination


class CategoryPagination(PageNumberPagination):
    """Пагинация для категорий"""
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class CategoryListView(generics.ListAPIView):
    """Эндпоинт для получения списка категорий с подкатегориями"""
    queryset = Category.objects.prefetch_related("subcategories").all()
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination
