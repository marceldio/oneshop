from django.urls import path
from shop.views import CategoryListView, ProductListView
from shop.views import CartView, AddToCartView, UpdateCartView, RemoveFromCartView, ClearCartView

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("products/", ProductListView.as_view(), name="product-list"),

    path("cart/", CartView.as_view(), name="cart-view"),
    path("cart/add/", AddToCartView.as_view(), name="add-to-cart"),
    path("cart/update/<int:product_id>/", UpdateCartView.as_view(), name="update-cart"),
    path("cart/remove/<int:product_id>/", RemoveFromCartView.as_view(), name="remove-from-cart"),
    path("cart/clear/", ClearCartView.as_view(), name="clear-cart"),
]
