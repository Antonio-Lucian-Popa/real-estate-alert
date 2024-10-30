from django.db import models


# Create your models here.
class Listing(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=100)
    url = models.URLField(unique=True)
    date_posted = models.DateTimeField()

    def __str__(self):
        return f"{self.title} - {self.price} EUR"


class SearchPreference(models.Model):
    city = models.CharField(max_length=100)
    max_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.city} - {self.max_price} EUR"
