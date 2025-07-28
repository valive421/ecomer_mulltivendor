from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Vendor model, links to User and stores vendor-specific info
class Vendor(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.TextField(null=True)
    mobile = models.PositiveBigIntegerField(unique=True,null=True, blank=True)
    ProfilePicture = models.ImageField(upload_to='vendor_profile_pictures/', null=True, blank=True)
    def __str__(self):
        return self.user.username
    
# Product category model
class Product_category(models.Model):
    title = models.CharField(max_length=200)
    detail = models.TextField(null=True)

    def __str__(self):
        return self.title
    

# Product model, links to category and vendor
class Product(models.Model):
    category = models.ForeignKey(Product_category,on_delete=models.SET_NULL,null=True,related_name='category_products')
    vendor = models.ForeignKey(Vendor,on_delete=models.SET_NULL,null=True)
    title = models.CharField(max_length=200)
    detail = models.TextField(null=True)
    price = models.FloatField()
    sells = models.PositiveIntegerField(default=0)
    listing_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    
# Customer model, links to User
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.PositiveBigIntegerField(unique=True)
    def __str__(self):
        return self.user.username
    
# Order model, links to Customer
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    ordertime = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=20, default='Pending')  
    def __unicode__(self):
        return '%s' % self.ordertime

# OrderItem model, links to Order and Product
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    price = models.FloatField()
    def __str__(self):
        return self.product.title
    
# CustomerAddress model, links to Customer
class CustomerAddress(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='customer_addresses', null=False, blank=False)
    address = models.TextField(null=True)
    default_address = models.BooleanField(default=False)

    def __str__(self):
        return self.address
    
# ProductRating model, links to Product and Customer
class ProductRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_ratings')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name='customer_ratings')
    rating = models.PositiveIntegerField()
    reviews = models.TextField(null=True)
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.reviews}-{self.rating}'
    
# ProductImage model, links to Product
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='product_images/')
    def __str__(self):
        return self.image.url

# ProfilePicture model, links to Customer
class ProfilePicture(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='profile_pictures')
    image = models.ImageField(upload_to='profile_pictures/')
    def __str__(self):
        return self.image.url


