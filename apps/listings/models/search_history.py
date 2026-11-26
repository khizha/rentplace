from django.conf import settings
from django.db import models

from apps.base.models import TimeStampModel


class SearchHistory(TimeStampModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='User',
        on_delete=models.CASCADE,
        related_name='search_history',
    )
    query = models.CharField(
        verbose_name='Search query',
        max_length=255,
    )

    class Meta:
        db_table = 'search_history'
        verbose_name = 'Search history'
        verbose_name_plural = 'Search history'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user}: {self.query}'