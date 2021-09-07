from movie_finder.models import Movie
from users.models import Watchlist, Review

Movie.objects.all().delete()
Watchlist.objects.all().delete()
Review.objects.all().delete()

print('Successful delete tables!')
