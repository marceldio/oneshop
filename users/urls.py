from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Получение access/refresh токенов
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Обновление access токена
]
