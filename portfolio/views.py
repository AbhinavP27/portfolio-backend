from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import AboutSection, Certificate, ContactMessage, Experience, HeroSection, Project, ProjectImage, Skill, ThemeSettings
from .serializers import (
    AboutSectionSerializer,
    CertificateSerializer,
    ContactMessageSerializer,
    ExperienceSerializer,
    HeroSectionSerializer,
    ProjectImageSerializer,
    ProjectSerializer,
    SkillSerializer,
    ThemeSettingsSerializer,
)


class HeroSectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HeroSection.objects.all().order_by('-updated_at', '-created_at')
    serializer_class = HeroSectionSerializer


class AboutSectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AboutSection.objects.all().order_by('-updated_at', '-created_at')
    serializer_class = AboutSectionSerializer


class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all().order_by('category', 'order', 'name')
    serializer_class = SkillSerializer


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.prefetch_related('images').all().order_by('category', 'order', '-featured', '-created_at')
    serializer_class = ProjectSerializer


class ProjectImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProjectImage.objects.select_related('project').all().order_by('project_id', 'order', 'id')
    serializer_class = ProjectImageSerializer


class ExperienceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Experience.objects.all().order_by('-start_date', 'order')
    serializer_class = ExperienceSerializer


class CertificateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Certificate.objects.all().order_by('-issue_date', 'order')
    serializer_class = CertificateSerializer


class ThemeSettingsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ThemeSettings.objects.all().order_by('-updated_at', '-created_at')
    serializer_class = ThemeSettingsSerializer

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


class ContactMessageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]
