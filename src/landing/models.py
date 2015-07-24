from django.db import models
from django.conf import settings

from raredoor.models import TimestampedModel


class Subscription(TimestampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    referer = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)

    def __unicode__(self):
        return str(self.pk) + ': ' + str(self.email)



class SubscriptionMerchant(Subscription):

    CATEGORY_DECOR = 1
    CATEGORY_ART = 2
    CATEGORY_FURNITURE = 3
    CATEGORY_VINTAGE = 4
    CATEGORY_FUN = 5

    CATEGORIES = (
      (CATEGORY_DECOR, 'Decor & Living'),
      (CATEGORY_ART, 'Art'),
      (CATEGORY_FURNITURE, 'Furniture'),
      (CATEGORY_VINTAGE, 'Vintage & Handmade'),
      (CATEGORY_FUN, 'Fun Stuff'),
    )

    title = models.CharField(max_length=8)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)

    phone = models.CharField(max_length=32)
    store = models.CharField(max_length=64)
    street = models.CharField(max_length=64, verbose_name='Address')
    street2 = models.CharField(max_length=64, verbose_name='Address 2', blank=True, null=True)
    zipcd = models.CharField(max_length=8, verbose_name='Zip')
    category = models.PositiveIntegerField(choices=CATEGORIES, blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'Mechant subscription'

    def __unicode__(self):
        return str(self.pk) + ': ' + self.store + ': ' + str(self.email)