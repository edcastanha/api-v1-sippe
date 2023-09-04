from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from core.cadastros.urls import router as cadastros_router
from core.cameras.urls import router as cameras_router

router = routers.DefaultRouter()
router.registry.extend(cadastros_router.registry)
router.registry.extend(cameras_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
