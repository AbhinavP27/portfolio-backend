from django.contrib import admin

from .models import (
    AboutSection,
    Certificate,
    ContactMessage,
    Experience,
    HeroSection,
    Project,
    ProjectImage,
    Skill,
    ThemeSettings,
)


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ('image', 'caption', 'order')


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('headline', 'contact_email', 'updated_at')
    search_fields = ('headline', 'subheadline', 'contact_email')


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ('heading', 'section_label', 'updated_at')
    search_fields = ('heading', 'description')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency', 'order')
    list_filter = ('category',)
    search_fields = ('name',)
    ordering = ('category', 'order', 'name')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'featured', 'order', 'updated_at')
    list_filter = ('category', 'featured')
    search_fields = ('title', 'slug', 'summary')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ('project', 'caption', 'order')
    list_filter = ('project',)
    ordering = ('project', 'order')


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('position', 'company', 'start_date', 'end_date', 'is_current', 'order')
    list_filter = ('is_current',)
    search_fields = ('position', 'company')
    ordering = ('-start_date', 'order')


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('title', 'issuer', 'issue_date', 'order')
    search_fields = ('title', 'issuer', 'credential_id')
    ordering = ('-issue_date', 'order')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at', 'updated_at')
    actions = ('mark_as_read', 'mark_as_unread')

    @admin.action(description='Mark selected messages as read')
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description='Mark selected messages as unread')
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)


@admin.register(ThemeSettings)
class ThemeSettingsAdmin(admin.ModelAdmin):
    list_display = ('theme_name', 'total_visitors', 'total_resume_downloads', 'updated_at')
    readonly_fields = ('total_visitors', 'total_resume_downloads')
