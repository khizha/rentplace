from django.db import models
from apps.listings.models.listing import Listing


class Features(models.Model):
    listing = models.OneToOneField(
        Listing,
        verbose_name='Listing',
        on_delete=models.CASCADE,
        related_name='features',
    )

    pets_allowed = models.BooleanField(
        verbose_name='Pets allowed',
        default=False,
    )
    smoking_allowed = models.BooleanField(
        verbose_name='Smoking allowed',
        default=False,
    )
    self_check_in = models.BooleanField(
        verbose_name='Self check-in',
        default=False,
    )
    wifi = models.BooleanField(
        verbose_name='Wi-Fi',
        default=False,
    )
    kitchen = models.BooleanField(
        verbose_name='Kitchen',
        default=False,
    )
    washing_machine = models.BooleanField(
        verbose_name='Washing machine',
        default=False,
    )
    free_parking = models.BooleanField(
        verbose_name='Free parking',
        default=False,
    )
    balcony = models.BooleanField(
        verbose_name='Balcony',
        default=False,
    )
    elevator = models.BooleanField(
        verbose_name='Elevator',
        default=False,
    )

    def __str__(self):
        return f'Features for {self.listing}'

    class Meta:
        db_table = 'housing_features'
        verbose_name = 'Housing features'
        verbose_name_plural = 'Housing features'