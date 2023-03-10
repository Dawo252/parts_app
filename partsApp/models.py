import datetime

from django.db import models
from django.contrib.postgres import fields
from django.db.models import F
from django.conf import settings


class Warehouse(models.Model):
    warehouse_name = models.CharField(max_length=100)
    warehouse_street = models.CharField(max_length=150)
    warehouse_open = models.BooleanField(default=True)


class Part(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='parts')
    producer_name = models.CharField(max_length=100)
    part_name = models.CharField(max_length=100)
    car = fields.ArrayField(models.CharField(max_length=50))
    price_netto = models.FloatField(default=0)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return self.part_name


class OrderPart(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    parts = models.ManyToManyField(OrderPart)
    start_date = models.DateTimeField(auto_now_add=True)
    order_date = models.DateTimeField(default=datetime.datetime)
    ordered = models.BooleanField(default=False)
