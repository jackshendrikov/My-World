from django.contrib import admin
from .models import Review, Watchlist

# Register your models here.
admin.site.register((Review, Watchlist))
