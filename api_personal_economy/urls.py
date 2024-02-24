from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from api_personal_economy import views

router = routers.DefaultRouter()
router.register(r'cuentas', views.CuentaViewSet)
router.register(r'operaciones', views.OperacionViewSet)
router.root_view_name = 'api-pe-root'

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]

