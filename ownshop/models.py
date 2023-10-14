from django.db import models
import email
from tabnanny import verbose
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager

# Create your models here.

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password,first_name,last_name,mobile, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        if not password:
            raise ValueError('The given password must be set')
        
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            mobile = mobile,
            password = password,
            **extra_fields
            )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password,first_name,last_name,mobile,**extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password,first_name,last_name,mobile,**extra_fields)

    def create_superuser(self, email, password,first_name,last_name,mobile,**extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password,first_name,last_name,mobile,**extra_fields)



class User(AbstractBaseUser,PermissionsMixin):

    email = models.EmailField(db_index=True,unique=True,max_length=50)
    first_name = models.CharField(max_length=50,blank=False,null=False)
    last_name = models.CharField(max_length=40,blank=False,null=False)
    mobile = models.CharField(max_length=50,blank=False,null=False)
    address = models.CharField(max_length=40,blank=False,null=False)
    password = models.CharField(max_length=40,blank=False,null=False)
    
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','mobile','password']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'



class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=100,default="")
    desc1 = models.CharField(max_length=800, default="")
    desc2 = models.CharField(max_length=800, default="")
    desc3 = models.CharField(max_length=800, default="")
    product_catagory = models.CharField(max_length=200, default="")
    product_sub_catagory = models.CharField(max_length=200, default="")
    product_price = models.FloatField(default=0)
    image = models.ImageField(upload_to='app/images', default="")

    def __str__(self):
        return self.product_name


class Contact(models.Model):
    msg_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=100,default="")
    email = models.CharField(max_length=200, default="")
    phone = models.CharField(max_length=200, default="")
    desc = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.name


class Customer(models.Model):
    cus_id = models.AutoField(primary_key = True)
    cus_name = models.CharField(max_length=100,default="")
    cus_email = models.CharField(max_length=200, default="")
    cus_password = models.CharField(max_length=50, default="")
    cus_phone = models.CharField(max_length=20, default="")
    cus_address = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.cus_name






class Order(models.Model):
    provider_order_id = models.CharField( max_length=40, null=False, blank=False)
    payment_id = models.CharField(max_length=36, null=False, blank=False )
    signature_id = models.CharField(max_length=128, null=False, blank=False)
    status =  models.BooleanField(default=False  )
    items_json = models.CharField(max_length=5000,default="")
    amount = models.IntegerField(default=0)
    email = models.CharField(max_length=100,default="")
    name = models.CharField(max_length=100,default="")
    address = models.CharField(max_length=1000, default="")
    city = models.CharField(max_length=500, default="")
    state = models.CharField(max_length=500, default="")
    zip_code = models.CharField(max_length=100,default="")
    mobile = models.CharField(max_length=20, default="")
    def __str__(self):
        return self.name
