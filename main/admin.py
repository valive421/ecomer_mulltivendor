from django.contrib import admin
from . import models

# Register Vendor, Product, and Product_category models
from django.contrib import admin
from .models import Vendor, Product_category, Product

admin.site.register(Vendor)  # Register Vendor model
admin.site.register(Product)  # Register Product model
admin.site.register(Product_category)  # Register Product_category model
admin.site.register(models.Customer)  # Register Customer model
admin.site.register(models.Order)  # Register Order model
admin.site.register(models.OrderItem)  # Register OrderItem model
admin.site.register(models.CustomerAddress)  # Register CustomerAddress model
admin.site.register(models.ProductRating)  # Register ProductRating model
admin.site.register(models.ProductImage)  # Register ProductImage model
admin.site.register(models.ProfilePicture)  # Register ProfilePicture model
