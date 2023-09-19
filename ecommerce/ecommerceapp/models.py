from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Package(models.Model):
    package_id = models.AutoField
    package_name = models.CharField(max_length=100)
    package_category = models.CharField(max_length=100, default="")
    # subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    image = models.ImageField(upload_to='images/images')
    
    def __str__(self):
        return self.package_category
    
class Contact(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    phone=models.IntegerField()
    message=models.TextField(max_length=500)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    package=models.CharField(max_length=50)
    address=models.TextField(max_length=500)
    payment=models.CharField(max_length=50)
    admission=models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural="Booked packages"

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to='profiles/%Y/%m/%d',null=True,blank=True)
    contact_number=models.CharField(max_length=15,null=True,blank=True)
    address=models.TextField(blank=True)
    updated_on=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name