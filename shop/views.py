from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, permissions, status
from shop.models import Category, Product, Cart
from shop.serializers import CategorySerializer, ProductSerializer, CartSerializer


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


class CartView(generics.ListAPIView):
    """Просмотр корзины пользователя"""
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class AddToCartView(APIView):
    """Добавление товара в корзину"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        if not product_id:
            return Response({"error": "Товар обязателен"}, status=status.HTTP_400_BAD_REQUEST)

        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response({"error": "Товар не найден"}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        return Response(CartSerializer(cart_item).data, status=status.HTTP_201_CREATED)


class UpdateCartView(APIView):
    """Изменение количества товара в корзине"""
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, product_id):
        cart_item = Cart.objects.filter(user=request.user, product_id=product_id).first()
        if not cart_item:
            return Response({"error": "Товар не найден в корзине"}, status=status.HTTP_404_NOT_FOUND)

        quantity = request.data.get("quantity")
        if not quantity or int(quantity) <= 0:
            cart_item.delete()
            return Response({"message": "Товар удалён из корзины"}, status=status.HTTP_204_NO_CONTENT)

        cart_item.quantity = int(quantity)
        cart_item.save()
        return Response(CartSerializer(cart_item).data)


class RemoveFromCartView(APIView):
    """Удаление товара из корзины"""
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, product_id):
        cart_item = Cart.objects.filter(user=request.user, product_id=product_id).first()
        if not cart_item:
            return Response({"error": "Товар не найден в корзине"}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()
        return Response({"message": "Товар удалён из корзины"}, status=status.HTTP_204_NO_CONTENT)


class ClearCartView(APIView):
    """Полная очистка корзины"""
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response({"message": "Корзина очищена"}, status=status.HTTP_204_NO_CONTENT)
