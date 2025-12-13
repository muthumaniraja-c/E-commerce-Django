from django.db import models
import datetime
import os
from django.contrib.auth.models import User
from itertools import product
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
def get_file_path(request,filename):
    original_filename = filename
    nowTime = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (nowTime,original_filename)
    return os.path.join('uploads/',filename)

class Category(models.Model):
    name = models.CharField(max_length=150,null=False,blank=False)
    image = models.ImageField(upload_to=get_file_path,null=True,blank=True)
    description = models.TextField(max_length=500, null=False,blank=False)
    status = models.BooleanField(default=False,help_text="0-show,1-Hidden")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=150,null=False,blank=False)
    vendor=models.CharField(max_length=150,null=False,blank=False)
    product_image = models.ImageField(upload_to=get_file_path,null=True,blank=True)
    quantity = models.IntegerField(null=False,blank=False)
    original_price=models.FloatField(null=False,blank=False)
    selling_price=models.FloatField(null=False,blank=False)
    description = models.TextField(max_length=500, null=False,blank=False)
    status = models.BooleanField(default=False,help_text="0-show,1-Hidden")
    trending = models.BooleanField(default=False,help_text="0-default,1-Trending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Cart(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  product=models.ForeignKey(Product,on_delete=models.CASCADE)
  product_qty=models.IntegerField(null=False,blank=False)
  created_at=models.DateTimeField(auto_now_add=True)
 
  @property
  def total_cost(self):
    return self.product_qty*self.product.selling_price
 
class Favourite(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	created_at=models.DateTimeField(auto_now_add=True)
 
class Order(models.Model):
    ORDER_STATUS = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=100, unique=True)
    
    # Shipping Information
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    
    # Order Information
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='Pending')
    payment_mode = models.CharField(max_length=50, default='Cash on Delivery')
    
    # Additional Information
    order_notes = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.order_number} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)  # Adjust to your Product model
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
@receiver(post_save, sender=Order)
def order_status_changed(sender, instance, created, **kwargs):
    """Send email when order status changes"""
    if not created:  # Only for updates, not new orders
        # Uncomment the line below to enable email notifications
        # send_order_status_email(instance)
        pass