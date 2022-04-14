from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Coin(models.Model):
    coinCode = models.CharField(max_length=10, primary_key=True)
    coinName = models.CharField(max_length=20, null=True)
    coinRate = models.FloatField(null=True)
    coinCap = models.IntegerField(null=True)
    coinVolume = models.IntegerField(null=True)
    coinIcon = models.URLField(null=True)


class Owns(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    quantity = models.DecimalField(default=0, decimal_places=10, max_digits=20)
# class Client(models.User):

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Delete profile when user is deleted
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile' #show how we want it to be displayed