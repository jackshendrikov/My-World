import difflib
import pandas as pd

from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Case, When

from .models import Movie
from users.models import Watchlist, MyRating
from users.models import Review

from jackshen.settings import SHEET_ID

values = ('imdb_id', 'title', 'rating_id__rating', 'link', 'votes', 'genres_id__genres', 'cast', 'runtime_id__runtime',
          'mtype_id__mtype', 'netflix_id__netflix', 'plot', 'keywords', 'release', 'year_id__year', 'poster',
          'youtube_id__youtube')

all_movies = Movie.objects.values_list(*values)

url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=904865657'
df_cast = pd.read_csv(url)['cast']
all_cast = list(
    set([j for sub in list(df_cast.str[2:-2].str.replace("'", "").str.replace('"', '').str.split(', ')) for j in sub])
)


# ========= UTILS ===========
def create_paginator(request, movies_list):
    page = request.GET.get('page', 1)
    movie_paginator = Paginator(movies_list, 15)

    try:
        movie_items = movie_paginator.page(page)
    except PageNotAnInteger:
        movie_items = movie_paginator.page(1)
    except EmptyPage:
        movie_items = movie_paginator.page(movie_paginator.num_pages)

    return movie_items


def get_watchlist(request):
    if request.user.is_authenticated:
        return list([x.movie_id for x in Watchlist.objects.filter(author=request.user)])
    else:
        return False


def get_my_rating(request):
    if request.user.is_authenticated:
        return list([x.movie_id for x in MyRating.objects.filter(user=request.user)])
    else:
        return False


# To get similar movies based on user rating
def get_similar(movie_name, rating, corr_matrix):
    similar_ratings = corr_matrix[movie_name]*(rating-2.5)
    similar_ratings = similar_ratings.sort_values(ascending=False)

    return similar_ratings


def get_corr_matrix():
    movie_rating = pd.DataFrame(list(MyRating.objects.all().values()))

    userRatings = movie_rating.pivot_table(index=['user_id'], columns=['movie_id'], values='rating')
    userRatings = userRatings.fillna(0, axis=1)
    corrMatrix = userRatings.corr(method='pearson')

    return corrMatrix


def get_recommendations(request, rec_num=100, order_by_votes=False):
    corrMatrix = get_corr_matrix()

    user = list(MyRating.objects.filter(user=request.user).values('id', 'user_id', 'movie_id', 'rating'))
    user = pd.DataFrame(user).drop(['user_id', 'id'], axis=1)

    user_filtered = [tuple(x) for x in user.values]
    movie_id_watched = [each[0] for each in user_filtered]

    similar_movies = pd.DataFrame()
    for movie, rating in user_filtered:
        similar_movies = similar_movies.append(get_similar(movie, rating, corrMatrix), ignore_index=True)

    movies_id = list(similar_movies.sum().sort_values(ascending=False).index)
    movies_id_recommend = [each for each in movies_id if each not in movie_id_watched][:100]
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(movies_id_recommend)])
    movie_list = all_movies.filter(imdb_id__in=movies_id_recommend).order_by(preserved)
    if order_by_votes:
        movie_list = movie_list.order_by('-votes')

    return list(movie_list[:rec_num])


# ========= VIEWS ===========
def get_category_movies(movie_list, request):
    my_watchlist = get_watchlist(request)
    movie_items = create_paginator(request, movie_list)

    return render(request, 'movie_finder/special-item.html', {'movieItems': movie_items, 'myWatchlist': my_watchlist})


@login_required
def my_ratings(request):
    my_watchlist = get_watchlist(request)
    my_rate = get_my_rating(request)

    user_ratings = [all_movies.get(imdb_id=val) for val in my_rate]
    count_rate = len(user_ratings)

    user_ratings = create_paginator(request, user_ratings)

    return render(request, 'movie_finder/watchlist_rating.html', {'userList': user_ratings,
                                                                  'myWatchlist': my_watchlist,
                                                                  'countList': count_rate,
                                                                  'keyword': 'Ratings'})


@login_required
def watchlist(request):
    my_watchlist = get_watchlist(request)

    if request.method == 'POST':
        imdb = request.POST.get('imdb')
        if imdb[:6] != "delete":
            movie = Movie.objects.get(imdb_id=imdb)
            if imdb not in my_watchlist:
                add_movie = Watchlist(movie=movie, author=request.user)
                messages.success(request, f'{movie.title} successfully added to your watchlist!')
                add_movie.save()
                return HttpResponse(status=204)
            else:
                messages.info(request, f'{movie.title} was already in your watchlist!')
                return redirect(request.META['HTTP_REFERER'])
        else:
            movie = Movie.objects.get(imdb_id=imdb[6:])
            delete_movie = Watchlist.objects.get(movie=movie, author=request.user)
            messages.error(request, f'{movie.title} has been deleted from your watchlist!')
            delete_movie.delete()
            return redirect(request.META['HTTP_REFERER'])

    user_watchlist = [all_movies.get(imdb_id=val) for val in my_watchlist]
    count_watchlist = len(user_watchlist)

    user_watchlist = create_paginator(request, user_watchlist)

    return render(request, 'movie_finder/watchlist_rating.html', {'userList': user_watchlist,
                                                                  'myWatchlist': my_watchlist,
                                                                  'countList': count_watchlist,
                                                                  'keyword': 'Watchlist'})


@login_required
def recommendations(request):
    my_watchlist = get_watchlist(request)
    my_rating = get_my_rating(request)

    if len(my_rating) < 10:
        messages.error(request, 'To get recommendations rate at least 10 movies.')
        return redirect(request.META['HTTP_REFERER'])

    movie_items = get_recommendations(request)
    movie_items = create_paginator(request, movie_items)

    return render(request, "movie_finder/special-item.html", {'movieItems': movie_items, 'myWatchlist': my_watchlist})


def main_page(request):
    if request.method == 'GET' and request.user.is_authenticated:
        my_watchlist = get_watchlist(request)
        my_rating = get_my_rating(request)

        movie_to_watch = list(all_movies.exclude(imdb_id__in=my_rating)
                              .filter(imdb_id__in=my_watchlist)
                              .order_by('-votes')
                              .order_by('-rating_id__rating')[:14])

        if len(movie_to_watch) < 14:
            movie_to_watch = False

        movie_list = False

        if len(my_rating) > 10:
            try:
                movie_list = get_recommendations(request, 14, True)
                if len(movie_list) < 14:
                    movie_list = False
            except Exception as e:
                print('Something went terribly wrong here!', e)

        return render(request, 'movie_finder/movies-main.html', {'movie2Watch': movie_to_watch,
                                                                 'myRecommendation': movie_list})

    return render(request, 'movie_finder/movies-main.html')


def category(request, category_name=None):
    if category_name == 'series':
        category_list = list(all_movies.filter(mtype_id__mtype='Series').order_by('-release'))
    elif category_name == 'netflix':
        category_list = list(all_movies.exclude(netflix_id__netflix='None').order_by('-rating_id__rating'))
    elif category_name == 'top':
        category_list = list(all_movies.order_by('-rating_id__rating')[:100])
    else:
        category_list = list(all_movies.filter(keywords__contains=category_name).order_by('-rating_id__rating'))

    return get_category_movies(category_list, request)


def advanced_search(request):
    my_watchlist = get_watchlist(request)
    my_rating = get_my_rating(request)

    movie_items = None
    get_cast = ''

    if request.method == 'GET':
        if request.GET.get('getYear') is not None or request.GET.get('getRate') is not None:
            get_rating = request.GET.get('getRate')
            get_year = request.GET.get('getYear')
            get_cast = request.GET.get('getCast')
            get_keywords = request.GET.get('getKeywords')
            get_genre = request.GET.get('getGenre')

            sorting = request.GET.get('sorting')
            exclude = request.GET.get('exclude')

            if get_cast:
                get_cast = difflib.get_close_matches(get_cast, all_cast)

                if len(get_cast) > 0:
                    get_cast = get_cast[0]
                else:
                    get_cast = 'No matches'
            else:
                get_cast = ''

            if get_genre == 'All': get_genre = ''
            if not get_year: get_year = 0
            if not get_rating: get_rating = 0.0

            rating = all_movies.filter(rating_id__rating__gte=float(get_rating))
            year = all_movies.filter(year_id__year__gte=float(get_year))
            genres = all_movies.filter(genres_id__genres__icontains=get_genre)
            cast = all_movies.filter(cast__icontains=get_cast)
            keywords = all_movies.filter(keywords__icontains=get_keywords)

            if exclude == 'excludeTitles':
                movie_items = all_movies.exclude(imdb_id__in=my_rating)
            else:
                movie_items = all_movies

            if sorting == 'byYear':
                movie_items = list(movie_items.intersection(rating, year, genres, cast, keywords).order_by('-release'))
            elif sorting == 'byVotes':
                movie_items = list(movie_items.intersection(rating, year, genres, cast, keywords).order_by('-votes'))
            else:
                movie_items = list(
                    movie_items.intersection(rating, year, genres, cast, keywords).order_by('-rating_id__rating'))

            movie_items = create_paginator(request, movie_items)

    return render(request, 'movie_finder/movies-list.html', {'getCast': get_cast, 'movieItems': movie_items,
                                                             'myWatchlist': my_watchlist})


def genre(request):
    my_watchlist = get_watchlist(request)
    movie_items = None
    genre_type = None

    if request.method == 'GET':
        if request.GET.get('typeGenre') is not None:
            genre_type = request.GET.get('typeGenre', 'False')
            movie_items = list(all_movies.filter(genres_id__genres__contains=genre_type).order_by('-rating_id__rating'))

            movie_items = create_paginator(request, movie_items)

    return render(request, 'movie_finder/special-item.html', {'movieItems': movie_items, 'genreType': genre_type,
                                                              'myWatchlist': my_watchlist})


def show_intro(request):
    youtube = request.POST.get('intro', 'False')
    title = request.POST.get('title', 'False')

    if youtube != 'False' and title != 'False':
        imdb = all_movies.get(title=title)[0]
        return render(request, "movie_finder/intro.html", {'youtube': "https://www.youtube.com/watch?v=" + youtube,
                                                           'title': title, 'imdb': imdb})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def result_page(request, movie_id: str):
    intro = request.POST.get('intro', False)

    if movie_id:
        my_watchlist = get_watchlist(request)
        if movie_id in my_watchlist:
            my_watchlist = True
        else:
            my_watchlist = False
        movie = all_movies.get(imdb_id=movie_id)
        search = list(movie)

        if request.user.is_authenticated and MyRating.objects.filter(movie=movie, user=request.user).exists():
            my_rating = MyRating.objects.get(movie=movie, user=request.user).rating
        else:
            my_rating = False

        imdb_id = search[0].strip()
        title = search[1].strip()
        rating = int(float(str(search[2]).strip()) * 10)
        link = search[3].strip()
        # votes = search[4]
        genres = search[5].strip()
        cast = search[6].strip()
        cast_list = cast[2:-2].replace("'", "").split(',')
        runtime = search[7]
        mType = search[8].strip()
        mNetflix = search[9].strip()
        plot = search[10].strip()
        year = search[13]
        poster = search[14].strip()
        if intro == 'noIntro':
            youtube = 'None'
            intro = 'Played'
        else:
            youtube = search[15].strip()
            intro = 'None'

        reviews = Review.objects.filter(movie=imdb_id)
        reviews_rate = False
        if reviews:
            reviews_rate = [(range(int(review.rating)), range(int(10 - review.rating))) for review in reviews]

        full_result = {'imdb_id': imdb_id, 'title': title, 'rating': rating, 'link': link, 'genres': genres,
                       'runtime': runtime, 'mtype': mType, 'netflix': mNetflix, 'plot': plot, 'poster': poster,
                       'year': year, 'youtube': youtube, 'cast_list': cast_list, 'reviews': reviews,
                       'reviews_rate': reviews_rate, 'intro': intro, 'my_rate': my_rating, 'inWatchlist': my_watchlist}

        return render(request, "movie_finder/result.html", full_result)
    else:
        messages.error(request, f'Error occurred while we\'re trying to show you info about the movie!')
        return redirect('/home/')


def movie_search(request):
    my_watchlist = get_watchlist(request)
    if request.GET:
        movie_items = False
        if ("q" in request.GET) and request.GET["q"].strip():
            query_title = request.GET["q"]
            found_movies = list(all_movies.filter(title__icontains=query_title).order_by('-rating_id__rating'))

            movie_items = create_paginator(request, found_movies)
    else:
        movie_items = False

    return render(request, "movie_finder/special-item.html", {'movieItems': movie_items, 'myWatchlist': my_watchlist})


def popular(request):
    my_watchlist = get_watchlist(request)
    # popular_url = 'https://s3.amazonaws.com/popular-movies/movies.json'
    # movies = json.loads(urlopen(popular_url).read().decode())
    # popular_movies = []
    #
    # for movie in movies:
    #     try:
    #         popular_movies.append(all_movies.get(title=movie['title']))
    #     except ObjectDoesNotExist:
    #         pass
    popular_movies = list(all_movies.order_by('-release'))[:30]

    return render(request, "movie_finder/special-item.html",
                  {'movieItems': popular_movies, 'myWatchlist': my_watchlist})
