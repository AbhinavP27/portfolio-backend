from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import AdminProfile
from .serializers import AdminProfileSerializer, AdminTokenObtainPairSerializer


class AdminTokenObtainPairView(TokenObtainPairView):
    serializer_class = AdminTokenObtainPairSerializer


class AdminTokenRefreshView(TokenRefreshView):
    pass


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile, _ = AdminProfile.objects.get_or_create(user=user, defaults={'display_name': user.username})
        data = AdminProfileSerializer(profile).data
        data['is_staff'] = user.is_staff
        return Response(data)
