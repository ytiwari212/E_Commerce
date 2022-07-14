import datetime
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


class Category(models.Model):
    name = models.CharField(max_length=250)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name


class Product(models.Model):
    uid = models.IntegerField(unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(
        Category, related_name="product_category", on_delete=models.CASCADE, default=1
    )
    description = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()


class Images(models.Model):
    product = models.ForeignKey(
        Product, related_name="product_image", on_delete=models.CASCADE, default=None
    )
    image = models.ImageField(upload_to="uploads/products/", blank=True)

    def __str__(self):
        return f"{self.product.name}-{self.image}"


class Order(models.Model):
    ORDER_STATUS = (
        ("Panding", "Panding"),
        ("Completed", "Completed"),
        ('Processing', 'Processing'),
    )

    # product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    # quantity = models.IntegerField(default=1)
    # price = models.IntegerField()
    date = models.DateField(default=datetime.datetime.today)
    # status = models.BooleanField(default=False)
    status = models.CharField(max_length=25, choices=ORDER_STATUS)
    # transaction_id = models.CharField(max_length=25, default='', blank=True)
    address = models.CharField(max_length=50, default="", blank=True)
    phone = models.CharField(max_length=50, default="", blank=True)

    def __str__(self):
        return f"{self.customer}-{self.date}"

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by("-date")


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)

    class Meta:
        unique_together = ("order", "product")
