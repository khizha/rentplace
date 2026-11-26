from django.conf import settings
from django.db import models

from apps.base.models import TimeStampModel
from apps.listings.models.listing import Listing


class ListingView(TimeStampModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='User',
        on_delete=models.CASCADE,
        related_name='listing_views',
    )
    listing = models.ForeignKey(
        Listing,
        verbose_name='Listing',
        on_delete=models.CASCADE,
        related_name='views',
    )

    class Meta:
        db_table = 'listing_views'
        verbose_name = 'Listing view'
        verbose_name_plural = 'Listing views'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} viewed {self.listing}'