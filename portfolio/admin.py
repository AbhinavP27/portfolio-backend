from django.contrib import admin

from .models import AboutSection, Certificate, ContactMessage, Experience, HeroSection, Project, Skill, ThemeSettings

admin.site.register(HeroSection)
admin.site.register(AboutSection)
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(Experience)
admin.site.register(Certificate)
admin.site.register(ContactMessage)
admin.site.register(ThemeSettings)
