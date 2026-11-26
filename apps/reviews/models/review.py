from django.db import models

from apps.base.models import TimeStampModel
from apps.bookings.models import Booking


class Review(TimeStampModel):
    booking = models.OneToOneField(
        Booking,
        verbose_name='Booking',
        on_delete=models.PROTECT,
        related_name='review',
    )

    rating = models.PositiveSmallIntegerField(
        verbose_name='Rating',
    )

    comment = models.TextField(
        verbose_name='Comment',
        blank=True,
    )

    class Meta:
        db_table = 'reviews'
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(
                condition=models.Q(rating__gte=1, rating__lte=5),
                name='review_rating_between_1_and_5',
            ),
        ]

    def __str__(self):
        return f'Review for booking {self.booking_id}'