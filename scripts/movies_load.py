import json
import requests
import urllib.request

from bs4 import BeautifulSoup
from imdb import IMDb
from collections import namedtuple
from datetime import datetime
from typing import Optional

from movie_finder.models import (
    Rate,
    Genre,
    Runtime,
    Type,
    Netflix,
    Year,
    Youtube,
    Movie,
)
from jackshen.settings import OMDB_API, OMDB_LINK, POPULAR_MOVIES_LINK
from home.utils.check_progress import print_progress

ia = IMDb()

MOVIE_INFO_COLUMNS = [
    "imdb_id",
    "title",
    "rating",
    "link",
    "votes",
    "genres",
    "cast",
    "runtime",
    "mtype",
    "netflix",
    "plot",
    "keywords",
    "release",
    "year",
    "poster",
    "youtube",
]

MovieInfo = namedtuple("Movie", MOVIE_INFO_COLUMNS)
all_movies_ids = Movie.objects.values_list("imdb_id", flat=True)


def retrieve_popular_movies_id_to_add(movies_ids: list) -> list:
    response = requests.get(POPULAR_MOVIES_LINK)
    soup = BeautifulSoup(response.text, "lxml")

    return [
        a.attrs.get("href").split("/")[2]
        for a in soup.select("td.titleColumn a")
        if a.attrs.get("href").split("/")[2] not in movies_ids
    ]


def create_movie_record(movie_id: str) -> Optional[MovieInfo]:
    json_data = (
        urllib.request.urlopen(OMDB_LINK.format(imdb_id=movie_id, api_key=OMDB_API))
        .read()
        .decode()
    )

    try:
        keywords = ia.get_movie(movie_id.strip()[2:], info="keywords")
        keywords = ", ".join(keywords["keywords"][:15])
    except KeyError:
        keywords = ""

    data = json.loads(json_data)

    if "Error" not in data.keys() and data["imdbRating"] != "N/A":
        return MovieInfo(
            imdb_id=data["imdbID"],
            title=data["Title"],
            rating=data["imdbRating"],
            link=f'https://www.imdb.com/title/{data["imdbID"]}',
            votes=data["imdbVotes"].replace(",", ""),
            genres=data["Genre"],
            cast=str(data["Actors"].replace("'", "`").split(", ")),
            runtime=data["Runtime"].split()[0],
            mtype=data["Type"].title(),
            netflix="None",
            plot=data["Plot"].replace('"', "'"),
            keywords=keywords,
            release=data["Released"],
            year=data["Year"].split("–")[0],
            poster=data["Poster"],
            youtube="None",
        )

    return None


movies_to_add = retrieve_popular_movies_id_to_add(all_movies_ids)
movies_len = len(movies_to_add)
print(f"{movies_len} movies will be added!")

print("Started..")
print_progress(0, movies_len, prefix="Progress:", suffix="Complete", length=50)
for i, movie_id in enumerate(movies_to_add):
    movie_info = create_movie_record(movie_id)
    if movie_info:
        rating, created = Rate.objects.get_or_create(rating=movie_info.rating)
        genres, created = Genre.objects.get_or_create(genres=movie_info.genres)
        runtime, created = Runtime.objects.get_or_create(runtime=movie_info.runtime)
        mtype, created = Type.objects.get_or_create(mtype=movie_info.mtype)
        netflix_link, created = Netflix.objects.get_or_create(
            netflix=movie_info.netflix
        )
        year, created = Year.objects.get_or_create(year=movie_info.year)
        youtube_link, created = Youtube.objects.get_or_create(
            youtube=movie_info.youtube
        )

        movie_date = datetime.strptime(movie_info.release, "%d %b %Y").strftime(
            "%Y-%m-%d"
        )

        Movie(
            imdb_id=movie_info.imdb_id,
            title=movie_info.title,
            rating=rating,
            link=movie_info.link,
            votes=movie_info.votes,
            genres=genres,
            cast=movie_info.cast,
            runtime=runtime,
            mtype=mtype,
            netflix=netflix_link,
            plot=movie_info.plot,
            keywords=movie_info.keywords,
            release=movie_date,
            year=year,
            poster=movie_info.poster,
            youtube=youtube_link,
        ).save()

    print_progress(i + 1, movies_len, prefix='Progress:', suffix='Complete', length=50)

print('Done!')
exit()
