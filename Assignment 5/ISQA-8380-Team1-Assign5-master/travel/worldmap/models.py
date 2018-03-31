from django.db import models
from django.contrib.auth.models import User
import decimal
# Create your models here.


class Region (models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=500, null=False)



class Location (models.Model):
    name = models.CharField(max_length=200, null=False)
    long = models.DecimalField(max_digits=50, decimal_places=2, null=False)
    lat = models.DecimalField(max_digits=50, decimal_places=2, null=False)
    type = models.CharField(max_length=200, null=False)
    rank = models.IntegerField()
    region = models.ForeignKey(Region, related_name='region')






class Visitor (models.Model):
    name = models.CharField(max_length=200, null=False)
    language = models.CharField(max_length=3, null=False)




class LocationVisitors (models.Model):
    location = models.ForeignKey(Location, related_name='location')
    visitor = models.ForeignKey(Visitor, related_name='visitor')