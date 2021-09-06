from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from movie_finder.models import Movie


class MyRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5, validators=[MaxValueValidator(10), MinValueValidator(0)])

    def __str__(self):
        return '{0}: {1}({2})'.format(self.user.username, self.movie.title, self.rating)


class Review(models.Model):
    movie = models.CharField(max_length=100, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0)
    review_description = models.TextField(default="")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    imdb = models.CharField(max_length=100, null=True)
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.author.username

    def save(self, *args, **kwargs):
        if not self.id:
            self.timestamp = timezone.now()
        self.timestamp = timezone.now()
        return super(Review, self).save(*args, **kwargs)


class Watchlist(models.Model):
    imdb = models.CharField(max_length=128, null=True)
    movie = models.CharField(max_length=100, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.movie + " - " + self.author.username
