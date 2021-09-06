from django.contrib import admin
from .models import Review, Watchlist, MyRating

# Register your models here.
admin.site.register((Review, Watchlist, MyRating))
