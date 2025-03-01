from rest_framework import serializers
from shop.models import Category, SubCategory, Product, Cart


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


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для продуктов"""
    category = serializers.StringRelatedField()
    subcategory = serializers.StringRelatedField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id", "name", "slug", "category", "subcategory", "price", "images")

    def get_images(self, obj):
        return {
            "small": obj.image_small.url if obj.image_small else None,
            "medium": obj.image_medium.url if obj.image_medium else None,
            "large": obj.image_large.url if obj.image_large else None,
        }


class CartSerializer(serializers.ModelSerializer):
    """Сериализатор для корзины"""
    product = serializers.StringRelatedField()
    product_id = serializers.IntegerField(source="product.id", read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ("product_id", "product", "quantity", "total_price")

    def get_total_price(self, obj):
        return obj.product.price * obj.quantity
