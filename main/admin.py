from django.contrib import admin
from . import models

from django.contrib import admin
from .models import Vendor, Product_category, Product

admin.site.register(Vendor)
admin.site.register(Product)
admin.site.register(Product_category)
admin.site.register(models.Customer)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.CustomerAddress)
admin.site.register(models.ProductRating)
admin.site.register(models.ProductImage)
