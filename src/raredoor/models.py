import uuid

from django.db import models
from django.conf import settings
from django.utils import timezone

from localflavor.us.models import PhoneNumberField


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(blank=False, null=False)
    updated_at = models.DateTimeField(blank=False, null=False)

    def save(self, *args, **kwargs):
        """Sets/updates created_at and updated_at timestamps"""

        right_now = timezone.now()
        if(not self.id):
            self.created_at = right_now
        self.updated_at = right_now
        super(TimestampedModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class PostalAddress(TimestampedModel): # UUIDModel, TimestampedModel
    street = models.CharField(max_length=50)
    street2 = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=2)  # TODO: needs list of choices here
    zipcd = models.IntegerField()
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    neighborhood = models.CharField(max_length=80)  # TODO: needs list of choices here


class ContactInfo(TimestampedModel): # UUIDModel, TimestampedModel
    phone = PhoneNumberField(blank=True, null=True, default='')
    sms_number = PhoneNumberField(blank=True, null=True, default='')
    email = models.EmailField(blank=True, null=True, default='')


def _generate_upload_to__abstract_image(instance, filename):
    name, ext = os.path.splitext(filename)
    return os.path.join('advisors', 'logo-' + str(uuid())  + ext)


class AbstractImageModel(models.Model):
    """
    Abstract image model for ProductImage and RetailerImage models.
    Uses AWS (before Cloudinary) as image store
    """
    #main image will be primary/1st displayed to user
    is_main = models.BooleanField(default=False)
    image = models.ImageField(blank=True, upload_to=_generate_upload_to__abstract_image)

    class Meta:
        abstract = True

