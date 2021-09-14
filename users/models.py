from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from movie_finder.models import Movie


class MyRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5, db_index=True, validators=[MaxValueValidator(10), MinValueValidator(0)])
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{0}: {1}({2})'.format(self.user.username, self.movie.title, self.rating)

    def save(self, *args, **kwargs):
        if not self.id:
            self.timestamp = timezone.now()
        self.timestamp = timezone.now()
        return super(MyRating, self).save(*args, **kwargs)


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5, validators=[MaxValueValidator(10), MinValueValidator(0)])
    review_description = models.TextField(default="")
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.author.username

    def save(self, *args, **kwargs):
        if not self.id:
            self.timestamp = timezone.now()
        self.timestamp = timezone.now()
        return super(Review, self).save(*args, **kwargs)


class Watchlist(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.movie.title + " - " + self.author.username

    def save(self, *args, **kwargs):
        if not self.id:
            self.timestamp = timezone.now()
        self.timestamp = timezone.now()
        return super(Watchlist, self).save(*args, **kwargs)
