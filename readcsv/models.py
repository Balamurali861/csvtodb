from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """DB model to register users
    is_superuser --> 1 - Authorised 2 -Unauthorised """

    username = models.CharField(unique=True,max_length=255, null=False)
    password = models.CharField(max_length=255, null=False)
    is_superuser = models.PositiveIntegerField(default=2)

    def __str__(self):
        return self.username

class File(models.Model):
    transaction_id = models.UUIDField(blank=False, null=False)
    transaction_time = models.DateTimeField(blank=False, null=False)
    product_name = models.CharField(max_length=255, blank=False, null=False)
    quantity = models.PositiveIntegerField(blank=False, null=False)
    unit_price = models.FloatField(blank=False, null=False)
    total_price = models.FloatField(blank=False, null=False)
    delivered_to_city = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.product_name


