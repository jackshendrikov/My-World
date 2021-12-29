import json
import urllib.request

from movie_finder.models import Movie
from jackshen.settings import OMDB_API, OMDB_API_2, OMDB_LINK
from home.utils.check_progress import print_progress

print_progress(0, Movie.objects.count(), prefix="Progress:", suffix="Complete", length=50)
for i, item in enumerate(Movie.objects.order_by('-release').iterator()):
    try:
        json_data = (
            urllib.request.urlopen(OMDB_LINK.format(imdb_id=item.imdb_id, api_key=OMDB_API))
                .read()
                .decode()
        )
    except Exception:
        json_data = (
            urllib.request.urlopen(OMDB_LINK.format(imdb_id=item.imdb_id, api_key=OMDB_API_2))
                .read()
                .decode()
        )

    data = json.loads(json_data)

    item.votes = data["imdbVotes"].replace(",", "")
    item.rating.rating = data["imdbRating"]
    item.save()
    print_progress(i + 1, Movie.objects.count(), prefix='Progress:', suffix='Complete', length=50)

print('Done!')
