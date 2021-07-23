from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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
    movie = models.CharField(max_length=100, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.movie + " - " + self.author.username
