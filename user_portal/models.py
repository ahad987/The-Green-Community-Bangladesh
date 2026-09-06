from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    """Optional volunteer information kept separate from Django's auth user."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='profiles/', blank=True)
    phone = models.CharField(max_length=40, blank=True)
    address = models.TextField(blank=True)
    education = models.CharField(max_length=255, blank=True)
    skills_interests = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Profile: {self.user.get_username()}'
