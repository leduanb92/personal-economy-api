from django.urls import include, path
from rest_framework import routers

from api_personal_economy import views

router = routers.DefaultRouter()
router.register(r'accounts', views.AccountsViewSet)
router.register(r'operations', views.OperationsViewSet)
router.root_view_name = 'api-pe-root'

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]

