from django.db import models
from django.core.validators import MinValueValidator
from django.utils.safestring import mark_safe

class electricalAppliances(models.Model):
    name = models.CharField(max_length=30, verbose_name = "Назва")
    power = models.IntegerField(validators=[MinValueValidator(1)], verbose_name = "Потужність (Вт)")
    duration = models.IntegerField(validators=[MinValueValidator(1)], default=50, verbose_name = "Тривалість роботи (хв)")


class Windmills(models.Model):
	name = models.CharField(max_length=30, verbose_name = "Назва")
	energy_character = models.FileField(upload_to='uploads/', null=True)
	#height =  models.IntegerField(validators=[MinValueValidator(1)], verbose_name = "Варіанти поставки ВЕУ з різними висотами башти")
	price_without_bashta = models.IntegerField(validators=[MinValueValidator(1)], verbose_name = "Вартість ВЕУ (без башти)")
	#price_bashta = models.IntegerField(validators=[MinValueValidator(1)], verbose_name = "Вартість башти")

class Tower(models.Model):
	height = models.IntegerField(validators=[MinValueValidator(1)], verbose_name = "Варіанти поставки ВЕУ з різними висотами башти")
	price = models.IntegerField(validators=[MinValueValidator(100)], verbose_name = "Ціна")
	windmills = models.ForeignKey(Windmills, on_delete=models.CASCADE)

