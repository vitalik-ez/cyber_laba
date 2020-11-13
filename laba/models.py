from django.db import models
from django.core.validators import MinValueValidator
from django.utils.safestring import mark_safe

class electricalAppliances(models.Model):
    name = models.CharField(max_length=30, verbose_name = "Назва")
    power = models.IntegerField(validators=[MinValueValidator(1)], verbose_name = "Потужність (Вт)")
    duration = models.IntegerField(validators=[MinValueValidator(1)], default=50, verbose_name = "Тривалість роботи (хв)")