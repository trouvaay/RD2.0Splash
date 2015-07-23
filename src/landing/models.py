from django.db import models
from django.conf import settings

from raredoor.models import TimestampedModel


class Subscription(TimestampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    referer = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(unique=True)

    def __unicode__(self):
        return str(self.pk) + ': ' + str(self.email)
