from django.urls import path

from .views import AdminTokenObtainPairView, AdminTokenRefreshView, MeView

urlpatterns = [
    path('login/', AdminTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', AdminTokenRefreshView.as_view(), name='token_refresh'),
    path('me/', MeView.as_view(), name='me'),
]
