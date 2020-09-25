from django.db import models

class Kyiv(models.Model):
	month = models.IntegerField()
	number_month = models.PositiveIntegerField()
	UTC = models.TimeField()
	T = models.IntegerField(null=True)
	dd = models.CharField(max_length=30, null=True)
	FF = models.IntegerField(null=True)