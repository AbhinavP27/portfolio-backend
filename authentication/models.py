from django.conf import settings
from django.db import models


class AdminProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='admin_profile')
    display_name = models.CharField(max_length=80, blank=True)
    title = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='admins/', blank=True, null=True)

    def __str__(self):
        return self.display_name or self.user.username
