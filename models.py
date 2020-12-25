from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.


class product(models.Model):
    name=models.CharField(max_length=100)
    title=models.TextField()
    offer_price=models.IntegerField()
    actual_price=models.IntegerField()
    img1=models.ImageField(upload_to='pics')
    img2=models.ImageField(upload_to='pics')
    img3=models.ImageField(upload_to='pics')
    brand=models.TextField()
    storage=models.TextField()
    ram=models.TextField()
    display=models.TextField()
    front_camera=models.TextField()
    back_camera=models.TextField()
    processor=models.TextField()
    battery=models.TextField()
    waranty=models.TextField()
    offer=models.BooleanField(default=False)
    rate=models.IntegerField()
    count=models.IntegerField()
    col=models.TextField()


class cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product_id = models.ForeignKey(product, on_delete=models.CASCADE)
    count=models.IntegerField(default=1)
    date= models.DateTimeField()

class card(models.Model):
    name=models.TextField()
    card_number=models.TextField()
    expiry=models.TextField()
    cvv=models.IntegerField()

class address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.TextField()
    mobileno=models.IntegerField()
    house_name=models.TextField()
    area=models.TextField()
    state=models.TextField()
    pincode=models.IntegerField()
    address_type=models.TextField()

class order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product= models.ForeignKey(product, on_delete=models.CASCADE)
    addres=models.ForeignKey(address, on_delete=models.CASCADE)
    amount=models.IntegerField()
    quantity=models.IntegerField()
    date=models.DateTimeField()
    status=models.TextField(default="packing")




