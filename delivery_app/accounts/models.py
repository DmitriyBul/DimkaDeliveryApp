from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import UserManager
# Create your models here.

from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    bonus_scores = models.IntegerField(default=0)
    objects = UserManager()

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)
