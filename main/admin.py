from django.contrib import admin
from . import models

from django.contrib import admin
from .models import Vendor, Product_category, Product

admin.site.register(Vendor)
admin.site.register(Product)
admin.site.register(Product_category)