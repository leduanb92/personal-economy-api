from django.urls import include, path
from django.contrib import admin
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
import api_personal_economy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pe/', include('api_personal_economy.urls')),
    path('users/', include('users.urls')),
    path('password-reset/', PasswordResetView.as_view()),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('login-token/', TokenObtainPairView.as_view(), name='login_token'),
    # path('refresh-token/', TokenRefreshView.as_view(), name='refresh_token'),
    # path('verify-token/', TokenVerifyView.as_view(), name='verify_token'),
]
