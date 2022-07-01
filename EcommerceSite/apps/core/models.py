from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth import get_user_model

# User = get_user_model()


class User(AbstractUser):
    mobile_number = models.CharField(
        max_length=40, unique=True, blank=False, null=False, db_index=True
    )
    address = models.CharField(max_length=255, blank=True, null=True)
    # REQUIRED_FIELDS = ["mobile_number", "email"]


    def __str__(self):
        return f"{self.first_name}/{self.mobile_number}/{self.email}"


# class Customer(models.Model):
#     name = models.CharField(max_length=200,null=True)
#     user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
#     date_created = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    name = models.CharField(max_length=250)
  
    @staticmethod
    def get_all_categories():
        return Category.objects.all()
  
    def __str__(self):
        return self.name


class Product(models.Model):
    uid = models.IntegerField(unique=True)
    name = models.CharField(max_length=255,blank=True, null=True)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, related_name="product_category", on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, blank=True, null=True)



class Images(models.Model):
    product = models.ForeignKey(Product, related_name="product_image", on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to='uploads/products/', blank=True)



# class Order(models.Model):
#     product = models.ForeignKey(Products,on_delete=models.CASCADE)
#     customer = models.ForeignKey(User, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     price = models.IntegerField()
#     date = models.DateField(default=datetime.datetime.today)
#     status = models.BooleanField(default=False)
  
#     def placeOrder(self):
#         self.save()
  
#     @staticmethod
#     def get_orders_by_customer(customer_id):
#         return Order.objects.filter(customer=customer_id).order_by('-date')