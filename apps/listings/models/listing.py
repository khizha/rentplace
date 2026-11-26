from django.conf import settings
from django.db import models

from apps.base.models import SoftDeleteModel, TimeStampModel
from apps.listings.choices.estate_type import EstateType


class Listing(TimeStampModel, SoftDeleteModel):
    title = models.CharField(
        verbose_name='Title',
        max_length=255,
    )

    description = models.TextField(
        verbose_name='Description',
    )

    street = models.ForeignKey(
        'listings.Street',
        verbose_name='Street',
        on_delete=models.PROTECT,
        related_name='listings',
    )

    house_number = models.CharField(
        verbose_name='House number',
        max_length=20,
        blank=True,
    )

    price = models.DecimalField(
        verbose_name='Price per night',
        max_digits=10,
        decimal_places=2,
    )

    rooms = models.PositiveSmallIntegerField(
        verbose_name='Number of rooms',
    )

    beds = models.PositiveSmallIntegerField(
        verbose_name='Number of beds',
    )

    bathrooms = models.PositiveSmallIntegerField(
        verbose_name='Number of bathrooms',
    )

    estate_type = models.CharField(
        verbose_name='Estate type',
        max_length=20,
        choices=EstateType.choices,
    )

    is_active = models.BooleanField(
        verbose_name='Is active',
        default=True,
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Owner',
        on_delete=models.PROTECT,
    )

    max_guests = models.PositiveSmallIntegerField(
        verbose_name='Maximum number of guests',
    )

    def __str__(self):
        return (
            f'{self.title} - {self.street.name}, '
            f'{self.street.district.name}, '
            f'{self.street.district.city.name}'
        )

    class Meta:
        db_table = 'listings'
        verbose_name = 'Listing'
        verbose_name_plural = 'Listings'
        default_related_name = 'listings'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gt=0),
                name='listing_price_gt_0',
            ),
            models.CheckConstraint(
                condition=models.Q(rooms__gte=1),
                name='listing_rooms_gte_1',
            ),
            models.CheckConstraint(
                condition=models.Q(bathrooms__gte=1),
                name='listing_bathrooms_gte_1',
            ),
            models.CheckConstraint(
                condition=models.Q(max_guests__gte=1),
                name='listing_max_guests_gte_1',
            ),
            models.CheckConstraint(
                condition=models.Q(
                    estate_type__in=EstateType.values
                ),
                name='listing_estate_type_valid',
            ),
        ]
        ordering = ['-created_at']
