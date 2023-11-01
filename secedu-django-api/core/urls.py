from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
#URLs API
from rest_framework import routers
from core.cadastros.urls import router as cadastros_router
from core.cameras.urls import router as cameras_router

#URLs ADMIN e SITE
from django.contrib import admin
from core.cameras import urls as cameras_urls
from core.cadastros import urls as cadastros_urls



# URLs DE API
router = routers.DefaultRouter()
router.registry.extend(cadastros_router.registry)
router.registry.extend(cameras_router.registry)

# URLS DE ADMIN e SITE
urlpatterns = [
    path('admin/', admin.site.urls),  # ADMIN
    path('api/v1/', include(router.urls)),  # API REST
    path('', include(cameras_urls)),  # SITE
    path('', include(cadastros_urls)),  # SITE
]

# INCLUDES static e media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
