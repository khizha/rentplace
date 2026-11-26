from django.db import models


class EstateType(models.TextChoices):
    APARTMENT = 'APARTMENT', 'Apartment'
    HOUSE = 'HOUSE', 'House'
    ROOM = 'ROOM', 'Room'
    STUDIO = 'STUDIO', 'Studio'