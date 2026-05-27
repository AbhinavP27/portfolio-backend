from django.db import connection
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AboutSection, Certificate, ContactMessage, Experience, HeroSection, Project, ProjectImage, Skill, ThemeSettings
from .permissions import AdminOnly, AdminWriteOrReadOnly
from .serializers import (
    CertificateSerializer,
    ContactMessageSerializer,
    ExperienceSerializer,
    AboutSectionSerializer,
    HeroSectionSerializer,
    ProjectSerializer,
    ProjectImageSerializer,
    SkillSerializer,
    ThemeSettingsSerializer,
)


class ReuseIdsOnSQLiteMixin:
    def _next_available_id(self):
        ids = list(self.get_queryset().order_by('id').values_list('id', flat=True))
        expected = 1
        for current in ids:
            if current != expected:
                return expected
            expected += 1
        return expected

    def _sync_sqlite_sequence(self, model):
        if connection.vendor != 'sqlite':
            return

        table = model._meta.db_table
        quoted_table = connection.ops.quote_name(table)

        with connection.cursor() as cursor:
            cursor.execute(f'SELECT MAX(id) FROM {quoted_table}')
            max_id = cursor.fetchone()[0]
            if max_id is None:
                cursor.execute('DELETE FROM sqlite_sequence WHERE name = %s', [table])
                return

            cursor.execute('UPDATE sqlite_sequence SET seq = %s WHERE name = %s', [max_id, table])
            if cursor.rowcount == 0:
                cursor.execute('INSERT INTO sqlite_sequence(name, seq) VALUES (%s, %s)', [table, max_id])

    def perform_create(self, serializer):
        if connection.vendor == 'sqlite':
            instance = serializer.save(id=self._next_available_id())
            self._sync_sqlite_sequence(instance.__class__)
            return
        serializer.save()

    def perform_destroy(self, instance):
        model = instance.__class__
        super().perform_destroy(instance)
        self._sync_sqlite_sequence(model)


class HeroSectionViewSet(ReuseIdsOnSQLiteMixin, viewsets.ModelViewSet):
    queryset = HeroSection.objects.all().order_by('-updated_at', '-created_at')
    serializer_class = HeroSectionSerializer
    permission_classes = [AdminWriteOrReadOnly]


class AboutSectionViewSet(ReuseIdsOnSQLiteMixin, viewsets.ModelViewSet):
    queryset = AboutSection.objects.all().order_by('-updated_at', '-created_at')
    serializer_class = AboutSectionSerializer
    permission_classes = [AdminWriteOrReadOnly]


class SkillViewSet(ReuseIdsOnSQLiteMixin, viewsets.ModelViewSet):
    queryset = Skill.objects.all().order_by('category', 'order', 'name')
    serializer_class = SkillSerializer
    permission_classes = [AdminWriteOrReadOnly]


class ProjectViewSet(ReuseIdsOnSQLiteMixin, viewsets.ModelViewSet):
    queryset = Project.objects.prefetch_related('images').all().order_by('category', 'order', '-featured', '-created_at')
    serializer_class = ProjectSerializer
    permission_classes = [AdminWriteOrReadOnly]


class ProjectImageViewSet(ReuseIdsOnSQLiteMixin, viewsets.ModelViewSet):
    queryset = ProjectImage.objects.select_related('project').all().order_by('project_id', 'order', 'id')
    serializer_class = ProjectImageSerializer
    permission_classes = [AdminWriteOrReadOnly]


class ExperienceViewSet(ReuseIdsOnSQLiteMixin, viewsets.ModelViewSet):
    queryset = Experience.objects.all().order_by('-start_date', 'order')
    serializer_class = ExperienceSerializer
    permission_classes = [AdminWriteOrReadOnly]


class CertificateViewSet(ReuseIdsOnSQLiteMixin, viewsets.ModelViewSet):
    queryset = Certificate.objects.all().order_by('-issue_date', 'order')
    serializer_class = CertificateSerializer
    permission_classes = [AdminWriteOrReadOnly]


class ThemeSettingsViewSet(ReuseIdsOnSQLiteMixin, viewsets.ModelViewSet):
    queryset = ThemeSettings.objects.all().order_by('-updated_at', '-created_at')
    serializer_class = ThemeSettingsSerializer
    permission_classes = [AdminWriteOrReadOnly]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def track_visit(self, request):
        theme = ThemeSettings.objects.order_by('-updated_at', '-created_at').first()
        if not theme:
            theme = ThemeSettings.objects.create()
        theme.total_visitors += 1
        theme.save(update_fields=['total_visitors', 'updated_at'])
        return Response({'total_visitors': theme.total_visitors})

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def track_resume_download(self, request):
        theme = ThemeSettings.objects.order_by('-updated_at', '-created_at').first()
        if not theme:
            theme = ThemeSettings.objects.create()
        theme.total_resume_downloads += 1
        theme.save(update_fields=['total_resume_downloads', 'updated_at'])
        return Response({'total_resume_downloads': theme.total_resume_downloads})


class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [AdminOnly()]

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return ContactMessage.objects.all()
        return ContactMessage.objects.none()

    @action(detail=True, methods=['post'], permission_classes=[AdminOnly])
    def mark_read(self, request, pk=None):
        message = self.get_object()
        message.is_read = True
        message.save(update_fields=['is_read', 'updated_at'])
        return Response({'status': 'read'})


class DashboardStatsView(APIView):
    permission_classes = [AdminOnly]

    def get(self, request):
        theme = ThemeSettings.objects.order_by('-updated_at', '-created_at').first()
        return Response(
            {
                'projects': Project.objects.count(),
                'featured_projects': Project.objects.filter(featured=True).count(),
                'skills': Skill.objects.count(),
                'messages_total': ContactMessage.objects.count(),
                'messages_unread': ContactMessage.objects.filter(is_read=False).count(),
                'experience_items': Experience.objects.count(),
                'certificates': Certificate.objects.count(),
                'visitor_statistics': theme.total_visitors if theme else 0,
                'resume_downloads': theme.total_resume_downloads if theme else 0,
            },
            status=status.HTTP_200_OK,
        )
