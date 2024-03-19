from django.db import models


class Location(models.Model):
    n = models.CharField(max_length=200)
    descriptioamen = models.TextField()
    address = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    event_name = models.CharField(max_length=200, blank=True, null=True)
    event_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=200)
    event_date = models.DateField()
    event_time = models.TimeField()

    def __str__(self):
        return self.event_name


class Imagine(models.Model):
    nume = models.CharField(max_length=255)
    imagine = models.BinaryField()

    def __str__(self):
        return self.nume