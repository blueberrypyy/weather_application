from django.db import models

class City(models.Model):
    name = models.CharField(max_length=25)
    account = models.IntegerField('City Account', blank=True, default=1)

    def __str__(self): # Show the actual city name on admin dashboard
        return self.name

    class Meta: # Show the plural of cities instead of citys
        verbose_name_plural = 'cities'

class Words(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
