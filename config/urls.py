from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/auth/', include('users.urls')),  # Эндпоинты для работы с токенами
    path("api/", include("shop.urls")),
]
