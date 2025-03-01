from rest_framework import serializers
from shop.models import Category, SubCategory


class SubCategorySerializer(serializers.ModelSerializer):
    """Сериализатор для подкатегорий"""

    class Meta:
        model = SubCategory
        fields = ("id", "name", "slug", "image")


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий, включает подкатегории"""
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "image", "subcategories")
