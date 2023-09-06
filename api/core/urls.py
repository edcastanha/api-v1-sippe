from django.urls import include, path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from core.cadastros.urls import router as cadastros_router
from core.cameras.urls import router as cameras_router

#URLs DE API
router = routers.DefaultRouter()
router.registry.extend(cadastros_router.registry)
router.registry.extend(cameras_router.registry)

#URLS DE ADMIN e SITE
urlpatterns = [
    #path('', include('admin_adminlte.urls')),
    path('admin/', admin.site.urls), #ADMIN
    path('api/', include(router.urls)), #API REST
]

# INCLUDES static e media
urlpatterns += [ 
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]

