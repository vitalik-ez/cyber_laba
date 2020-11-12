from django.db import models
from django.core.validators import MinValueValidator

class electricalAppliances(models.Model):
    name = models.CharField(max_length=30)
    power = models.IntegerField(validators=[MinValueValidator(1)])
    duration = models.IntegerField(validators=[MinValueValidator(1)], default=50)