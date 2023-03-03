from django.db import models
from django.contrib.postgres import fields
from django.db.models import F

class Warehouse(models.Model):
    warehouse_name = models.CharField(max_length=100)
    warehouse_street = models.CharField(max_length=150)
    warehouse_open = models.BooleanField(default=True)


class Part(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='parts')
    producer_name = models.CharField(max_length=100)
    part_name = models.CharField(max_length=100)
    car = fields.ArrayField(models.CharField(max_length=50))
    price_netto = models.FloatField()
    amount = models.IntegerField(default=0)

    def __str__(self):
        return self.part_name
