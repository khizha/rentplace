from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.base.models import TimeStampModel
from apps.bookings.choices.booking_status import BookingStatus
from apps.listings.models import Listing


class Booking(TimeStampModel):
    start_date = models.DateField(
        verbose_name='Start date',
    )

    end_date = models.DateField(
        verbose_name='End date',
    )

    cancelled_at = models.DateTimeField(
        verbose_name='Cancelled at',
        null=True,
        blank=True,
    )

    price_per_night = models.DecimalField(
        verbose_name='Price per night',
        max_digits=10,
        decimal_places=2,
    )

    status = models.CharField(
        verbose_name='Booking status',
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING,
    )

    rejection_reason = models.TextField(
        verbose_name='Rejection reason',
        blank=True,
    )

    listing = models.ForeignKey(
        Listing,
        verbose_name='Listing',
        on_delete=models.PROTECT,
        related_name='bookings',
    )

    renter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Renter',
        on_delete=models.PROTECT,
        related_name='bookings',
    )

    class Meta:
        db_table = 'bookings'
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(
                condition=models.Q(end_date__gt=models.F('start_date')),
                name='booking_end_date_after_start_date',
            ),
            models.CheckConstraint(
                condition=models.Q(status__in=BookingStatus.values),
                name='booking_status_valid',
            ),
        ]

    def clean(self):
        super().clean()

        errors = {}

        if self.listing_id and self.renter_id:
            if self.listing.owner_id == self.renter_id:
                errors['renter'] = 'You cannot book your own listing.'

        today = timezone.localdate()

        if self.start_date and self.start_date < today:
            errors['start_date'] = 'Start date cannot be in the past.'

        if self.end_date and self.end_date < today:
            errors['end_date'] = 'End date cannot be in the past.'

        if errors:
            raise ValidationError(errors)


    def __str__(self):
        return (
            f'{self.renter} - {self.listing} '
            f'({self.start_date} to {self.end_date})'
        )