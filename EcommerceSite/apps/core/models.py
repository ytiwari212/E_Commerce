import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator



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
    date = models.DateField(default=datetime.datetime.today)
    status = models.CharField(max_length=25, choices=ORDER_STATUS)
    # transaction_id = models.CharField(max_length=25, default='', blank=True)
    address = models.CharField(max_length=50, default="", blank=True)
    phone = models.CharField(max_length=50, default="", blank=True)
    apply_coupon= models.BooleanField(default=False)

    def __str__(self):
        return f"ID:{self.id}----CUSTOMER:{self.customer}"

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by("-date")


class Coupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=15)
    amount = models.FloatField()
    valid_from = models.DateTimeField(null=True)
    valid_to = models.DateTimeField(null=True)
    max_value = models.IntegerField(validators=[MaxValueValidator(10)], verbose_name='Coupon Quantity', null=True) # No. of coupon
    used = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.code}-{self.user.first_name}"


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    total_amount = models.FloatField(null=True,blank=True)
    coupon = models.ForeignKey(Coupon, related_name="order_coupon", on_delete=models.CASCADE, null=True)


    class Meta:
        unique_together = ("order", "product")




