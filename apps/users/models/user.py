from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Lower

from apps.base.models import TimeStampModel


class User(AbstractUser, TimeStampModel):
    email = models.EmailField(
        verbose_name='Email address',
        unique=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta(AbstractUser.Meta):
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

        constraints = [
            models.UniqueConstraint(
                Lower('email'),
                name='email_unique_lowercase',
            ),
        ]

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    def has_role(self, role):
        return self.groups.filter(name=role).exists()