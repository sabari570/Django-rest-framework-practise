from django.db import models
from django.conf import settings

# Create your models here.
# This is how we actually import the user model
User = settings.AUTH_USER_MODEL


class Product(models.Model):
    # pk -> default primary_key which is an integer
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=00.00)
    public = models.BooleanField(default=True)
    # creating a user field in the products table
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)

    # the @property creates a new field named sale_price, that returns the operation we have performed in it
    @property
    def sale_price(self):
        return "%.2f" % (float(self.price) * 0.6)

    # This is a function written in the model inorder to get some value based on some calculations
    # Its not a property it just returns some value we need for operations
    def get_discount(self):
        return "80"
