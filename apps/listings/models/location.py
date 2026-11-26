from django.db import models


class City(models.Model):  # City - unique
    name = models.CharField(
        verbose_name='City',
        max_length=100,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cities'
        verbose_name = 'City'
        verbose_name_plural = 'Cities'


class District(models.Model):
    # A district is associated with a city. The name of a district may appear in different cities.
    city = models.ForeignKey(
        City,
        verbose_name='City',
        on_delete=models.CASCADE,
        related_name='districts',
    )
    name = models.CharField(
        verbose_name='District',
        max_length=100,
    )

    def __str__(self):
        return f'{self.name}, {self.city}'

    class Meta:
        db_table = 'districts'
        verbose_name = 'District'
        verbose_name_plural = 'Districts'
        constraints = [
            models.UniqueConstraint(
                fields=['city', 'name'],
                name='unique_district_per_city',
            ),
        ]


class Street(models.Model):
    # A street is associated with a district. A street may appear in different districts.
    district = models.ForeignKey(
        District,
        verbose_name='District',
        on_delete=models.CASCADE,
        related_name='streets',
    )
    name = models.CharField(
        verbose_name='Street',
        max_length=255,
    )

    def __str__(self):
        return f'{self.name}, {self.district}'

    class Meta:
        db_table = 'streets'
        verbose_name = 'Street'
        verbose_name_plural = 'Streets'
        constraints = [
            models.UniqueConstraint(
                fields=['district', 'name'],
                name='unique_street_per_district',
            ),
        ]