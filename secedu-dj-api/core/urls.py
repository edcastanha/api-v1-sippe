from django.urls import include, path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from core.cadastros.urls import router as cadastros_router
from core.cameras.urls import router as cameras_router
from core.webApp import urls as webApp

# URLs DE API
router = routers.DefaultRouter()
router.registry.extend(cadastros_router.registry)
router.registry.extend(cameras_router.registry)

# URLS DE ADMIN e SITE
urlpatterns = [
    path('admin/', admin.site.urls),  # ADMIN
    path('api/v1/', include(router.urls)),  # API REST
    path('cadastros/', include(webApp)),
]

# INCLUDES static e media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
