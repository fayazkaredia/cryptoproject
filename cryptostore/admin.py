from django.contrib import admin
from cryptostore.models import Coin, Owns,Profile

# Register your models here.

admin.site.register(Coin)
admin.site.register(Owns)
admin.site.register(Profile)