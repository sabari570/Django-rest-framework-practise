from django.db import models
from django.conf import settings
from django.db.models import Q

# Create your models here.
# This is how we actually import the user model
User = settings.AUTH_USER_MODEL

# We are implementing a search filter for the products for that first we need to make some modifications in the
# Product models file


# This the ProductQuerySet class where we actually define what the get_queryset function inside the ProductManager is supposed to return
# the self.get_queryset() inside the ModelManager refers to the Queryset methods that are defined inside the ProductQuerySet class that inherits the models.QuerySet
# this class is used to customize, how we must query the data from the db, as in what all filters must be applied an all.
class ProductQuerySet(models.QuerySet):

    # This function returns a query which filters the Products data based on the public field
    def is_public(self):
        return self.filter(public=True)

    # This is the where the search logic is written while querying the products
    # this function first filters the products based on the public field and then based on the query
    # and if the user is present it first filters the query based on the user data
    # and then it filters it based on the query, so now we have two queries one with the is_public and then query
    # the other with the user-data and the query, finally we combine them both and then select the disticnt of them that is only select the unique ones
    # common ones are selected only once.
    def search(self, query, user=None):
        # Here Q is used because - It allows you to build complex queries that include logical operations (AND, OR, and NOT) for combining multiple conditions.
        # here we perform an OR operation because, It checks whether the title contains the query (case-insensitive).
        # OR the content contains the query (case-insensitive).
        lookup = Q(title__icontains=query) | Q(content__icontains=query)
        qs = self.is_public().filter(lookup)
        if user is not None:
            # qs_with_user: Filters records specific to the user (self.filter(user=user)) and applies the lookup condition.
            qs_with_user = self.filter(user=user).filter(lookup)
            # .distinct(): Ensures no duplicate records in the final result.
            qs = (qs | qs_with_user).distinct()
        return qs


# This is the ProductManager class which is actually used in the Product model inorder to implement the search feature
# * Acts as a bridge between the Product model and the custom queryset (ProductQuerySet).
# * Manages how queries are built and ensures that the custom queryset is used when querying the model.
# this function returns the ProductQuerySet instance, in which we have the functions that applies the filters
class ProductManager(models.Manager):
    # the get_queryset() is the default function that is present in the Manager model
    # and the logics of this function can be customized by the QuerySet model class written above
    def get_queryset(self, *args, **kwargs):
        # The using=self._db argument in the ProductQuerySet constructor is used to specify which database connection the queryset should use when executing queries
        # In Django, you can define multiple database connections in the DATABASES setting, and each connection has an alias (e.g., 'default', 'replica', 'archive').
        # When a query is executed, Django needs to know which database connection to use. self._db ensures the query is executed on the correct database.
        return ProductQuerySet(self.model, using=self._db)

    # This function now uses the search function that is defined inside the ProductQuerySet
    def search(self, query, user=None):
        # Here the self.get_queryset() return the ProductQuerySet instace
        return self.get_queryset().search(query, user=user)


class Product(models.Model):
    # pk -> default primary_key which is an integer
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=00.00)
    public = models.BooleanField(default=True)
    # creating a user field in the products table
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)

    # This is how we link the ProductManager with the Product model
    objects = ProductManager()

    # the @property creates a new field named sale_price, that returns the operation we have performed in it
    @property
    def sale_price(self):
        return "%.2f" % (float(self.price) * 0.6)

    # This is a function written in the model inorder to get some value based on some calculations
    # Its not a property it just returns some value we need for operations
    def get_discount(self):
        return "80"
