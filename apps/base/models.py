from django.db import models
from django.utils import timezone


class TimeStampModel(models.Model):
    created_at = models.DateField(
        verbose_name='Created at',
        auto_now_add=True,
    )
    updated_at = models.DateField(
        verbose_name='Updated at',
        auto_now=True,
    )

    class Meta:
        abstract = True



class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return self.update(deleted_at=timezone.localdate())

    def hard_delete(self):
        return super().delete()

    def restore(self):
        return self.update(deleted_at=None)

    def alive(self):
        return self.filter(deleted_at__isnull=True)

    def deleted(self):
        return self.filter(deleted_at__isnull=False)


class SoftDeleteManager(models.Manager.from_queryset(SoftDeleteQuerySet)):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class SoftDeleteModel(models.Model):
    deleted_at = models.DateField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = SoftDeleteQuerySet.as_manager()

    class Meta:
        abstract = True

    @property
    def is_deleted(self):
        return self.deleted_at is not None

    def delete(self):
        self.deleted_at = timezone.localdate()
        self.save(update_fields=['deleted_at'])

    def hard_delete(self):
        return super().delete()

    def restore(self):
        self.deleted_at = None
        self.save(update_fields=['deleted_at'])