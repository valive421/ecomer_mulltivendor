from django.db import models
from django.contrib.auth.models import User

#vendor model
class Vendor(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.TextField(null=True)
    def __str__(self):
        return self.user.username
    
class Product_category(models.Model):
    title = models.CharField(max_length=200)
    detail = models.TextField(null=True)

    def __str__(self):
        return self.title
    

class Product(models.Model):
    category = models.ForeignKey(Product_category,on_delete=models.SET_NULL,null=True,related_name='category_products')
    vendor = models.ForeignKey(Vendor,on_delete=models.SET_NULL,null=True)
    title = models.CharField(max_length=200)
    detail = models.TextField(null=True)
    price = models.FloatField()
    sells = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.title
    
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.PositiveBigIntegerField(unique=True)

    def __str__(self):
        return self.user.username
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    ordertime = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=20, default='Pending')  # e.g., Pending, Completed, Cancelled
    def __unicode__(self):
        return '%s' % self.ordertime

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    price = models.FloatField()
    def __str__(self):
        return self.product.title
    
class CustomerAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name='customer_addresses')
    address = models.TextField(null=True)
    default_address = models.BooleanField(default=False)

    def __str__(self):
        return self.address
    
class ProductRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_ratings')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name='customer_ratings')
    rating = models.PositiveIntegerField()
    reviews = models.TextField(null=True)
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.reviews}-{self.rating}'
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='product_images/')
    def __str__(self):
        return self.image.url

