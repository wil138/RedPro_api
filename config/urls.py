from django.urls import path, include
from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta al panel de administración

    # 1. Tráfico para tu API:
   # path('api/', include('RedPro_api.urls')),  # Correcto: incluye las rutas de la app

    # 2. Rutas de Autenticación JWT:
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]