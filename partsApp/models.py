from django.db import models
from django.contrib.postgres import fields
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField


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
    discount_price = models.FloatField(blank=True, null=True)
    amount = models.IntegerField(default=0)
    slug = models.SlugField()
    description = models.TextField()
    photo = models.ImageField(upload_to="images/", null=True)

    def __str__(self):
        return self.part_name

    def get_absolute_url(self):
        return reverse("partsApp:part", kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse("partsApp:add_to_cart", kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse("partsApp:remove_from_cart", kwargs={'slug': self.slug})

    def get_photo(self):
        return self.photo.url


class OrderPart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def get_total_part_price(self):
        return self.part.price_netto * self.quantity


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parts = models.ManyToManyField(OrderPart)
    start_date = models.DateTimeField(auto_now_add=True)
    order_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)

    def get_the_total_price(self):
        total_price = 0
        for order_part in self.parts.all():
            total_price += order_part.get_total_part_price()
        return total_price

    def get_total_parts_quant(self):
        quant = 0
        for order_part in self.parts.all():
            quant += order_part.quantity
        return quant


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    # both solutions below are ok
    # country = forms.ChoiceField(widget=widgets.CountrySelectWidget, choices=countries)  # -> handled with django-countries
    country = CountryField(multiple=False)  # -> handled with django-countries
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.name
