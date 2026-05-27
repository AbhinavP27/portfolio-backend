from django.urls import include, path
from rest_framework.routers import DefaultRouter

from portfolio.views import (
    AboutSectionViewSet,
    CertificateViewSet,
    ContactMessageViewSet,
    DashboardStatsView,
    ExperienceViewSet,
    HeroSectionViewSet,
    ProjectViewSet,
    ProjectImageViewSet,
    SkillViewSet,
    ThemeSettingsViewSet,
)

router = DefaultRouter()
router.register('hero', HeroSectionViewSet, basename='hero')
router.register('about', AboutSectionViewSet, basename='about')
router.register('skills', SkillViewSet, basename='skills')
router.register('projects', ProjectViewSet, basename='projects')
router.register('project-images', ProjectImageViewSet, basename='project-images')
router.register('experience', ExperienceViewSet, basename='experience')
router.register('certificates', CertificateViewSet, basename='certificates')
router.register('messages', ContactMessageViewSet, basename='messages')
router.register('theme', ThemeSettingsViewSet, basename='theme')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
]
