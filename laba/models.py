from django.db import models
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from django.utils.safestring import mark_safe

class electricalAppliances(models.Model):
    name = models.CharField(max_length=30, verbose_name = "Назва")
    power = models.IntegerField(validators=[MinValueValidator(1)], verbose_name = "Потужність (Вт)")
    duration = models.IntegerField(validators=[MinValueValidator(1)], default=50, verbose_name = "Тривалість роботи (хв)")


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.xlsx', '.xls']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')





class Windmills(models.Model):
	name = models.CharField(max_length=30, verbose_name = "Назва")
	energy_character = models.FileField(upload_to='energy_characteristic/', null=True, verbose_name = "Енергетична характеристика ВЕУ (добавте файл у форматі xls)", validators=[validate_file_extension])
	#height =  models.IntegerField(validators=[MinValueValidator(1)], verbose_name = "Варіанти поставки ВЕУ з різними висотами башти")
	price_without_bashta = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000000)], verbose_name = "Вартість ВЕУ (без башти)")
	#price_bashta = models.IntegerField(validators=[MinValueValidator(1)], verbose_name = "Вартість башти")

class Tower(models.Model):
	height = models.IntegerField(verbose_name = "Висота башти", validators=[MinValueValidator(50), MaxValueValidator(300)])
	price = models.IntegerField(verbose_name = "Вартість башти", validators=[MinValueValidator(1), MaxValueValidator(1000000)])
	#windmills = models.ForeignKey(Windmills, on_delete=models.CASCADE)
	windmills = models.IntegerField()



class TowerNew(models.Model):
	height = models.IntegerField(verbose_name = "Висота new башти")
	price = models.IntegerField(verbose_name = "Вартість new башти")
	#windmills = models.ForeignKey(Windmills, on_delete=models.CASCADE)
	windmills = models.IntegerField(verbose_name = "Який вітряк")

