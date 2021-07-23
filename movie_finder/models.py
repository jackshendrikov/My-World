import uuid
import datetime
from django.db import models


class Rate(models.Model):
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)


class Genre(models.Model):
    genres = models.TextField()

    def __str__(self):
        return self.genres


class Runtime(models.Model):
    runtime = models.IntegerField(null=True)


class Type(models.Model):
    mtype = models.CharField(max_length=128)

    def __str__(self):
        return self.mtype


class Netflix(models.Model):
    netflix = models.TextField()

    def __str__(self):
        return self.netflix


class Year(models.Model):
    year = models.IntegerField(null=True)


class Youtube(models.Model):
    youtube = models.TextField()

    def __str__(self):
        return self.youtube


class Movie(models.Model):
    imdb_id = models.CharField(max_length=128, unique=True, default=uuid.uuid4, primary_key=True)
    title = models.CharField(max_length=256)
    link = models.TextField()
    votes = models.IntegerField(null=True, blank=True)
    cast = models.TextField()
    plot = models.TextField()
    keywords = models.TextField()
    poster = models.TextField()
    release = models.DateField(default=datetime.date.today)

    rating = models.ForeignKey(Rate, on_delete=models.CASCADE)
    genres = models.ForeignKey(Genre, on_delete=models.CASCADE)
    runtime = models.ForeignKey(Runtime, on_delete=models.CASCADE)
    mtype = models.ForeignKey(Type, on_delete=models.CASCADE)
    netflix = models.ForeignKey(Netflix, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    youtube = models.ForeignKey(Youtube, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
