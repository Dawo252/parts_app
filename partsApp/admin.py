from django.contrib import admin
from .models import Warehouse, Part, Order, OrderPart

admin.site.register(Part)
admin.site.register(Warehouse)
admin.site.register(Order)
admin.site.register(OrderPart)
