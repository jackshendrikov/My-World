import difflib
import pandas as pd

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Movie
from users.models import Watchlist
from users.models import Review

from jackshen.settings import SHEET_ID

values = ('imdb_id', 'title', 'rating_id__rating', 'link', 'votes', 'genres_id__genres', 'cast', 'runtime_id__runtime',
          'mtype_id__mtype', 'netflix_id__netflix', 'plot', 'keywords', 'release', 'year_id__year', 'poster',
          'youtube_id__youtube')

all_movies = Movie.objects.values_list(*values)

url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=904865657'
df_cast = pd.read_csv(url)['cast']
all_cast = list(set([j for sub in list(df_cast.str[2:-2].str.replace("'", "").str.replace('"', '').str.split(', ')) for j in sub]))


def get_watchlist(request):
    if request.user.is_authenticated:
        return list([x.imdb for x in Watchlist.objects.filter(author=request.user)])
    else: return False


def get_category_movies(movie_list, request):
    my_watchlist = get_watchlist(request)

    page = request.GET.get('page', 1)
    paginator_category = Paginator(movie_list, 15)

    try:
        movie_items = paginator_category.page(page)
    except PageNotAnInteger:
        movie_items = paginator_category.page(1)
    except EmptyPage:
        movie_items = paginator_category.page(paginator_category.num_pages)

    return render(request, 'movie_finder/special-item.html', {'movieItems': movie_items, 'myWatchlist': my_watchlist})


@login_required
def watchlist(request):
    my_watchlist = get_watchlist(request)

    if request.method == 'POST':
        movie = request.POST.get('movie')
        imdb = request.POST.get('imdb')
        if movie[:6] != "delete":
            if imdb not in my_watchlist:
                add_movie = Watchlist(imdb=imdb, movie=movie, author=request.user)
                messages.success(request, f'{movie} successfully added to your watchlist!')
                add_movie.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                messages.info(request, f'{movie} was already in your watchlist!')
                return redirect(request.META['HTTP_REFERER'])
        else:
            delete_movie = Watchlist.objects.get(imdb=imdb, movie=movie[6:], author=request.user)
            messages.error(request, f'{movie[6:]} has been deleted from your watchlist!')
            delete_movie.delete()
            return redirect(request.META['HTTP_REFERER'])

    user_watchlist = [all_movies.get(imdb_id=val) for val in my_watchlist]

    page = request.GET.get('page', 1)
    paginator_watchlist = Paginator(user_watchlist, 15)

    try:
        user_watchlist = paginator_watchlist.page(page)
    except PageNotAnInteger:
        user_watchlist = paginator_watchlist.page(1)
    except EmptyPage:
        user_watchlist = paginator_watchlist.page(paginator_watchlist.num_pages)

    return render(request, 'movie_finder/watchlist.html', {'userWatchlist': user_watchlist, 'myWatchlist': my_watchlist})


def main_page(request):
    return render(request, 'movie_finder/movies-main.html')


def halloween(request):
    halloween_list = list(all_movies.filter(keywords__contains='halloween-category').order_by('-rating_id__rating'))
    return get_category_movies(halloween_list, request)


def xmas(request):
    xmas_list = list(all_movies.filter(keywords__contains='xmas-category').order_by('-rating_id__rating'))
    return get_category_movies(xmas_list, request)


def all_series(request):
    series_list = list(all_movies.filter(mtype_id__mtype='Series').order_by('-release'))
    return get_category_movies(series_list, request)


def netflix(request):
    netflix_movies = list(all_movies.exclude(netflix_id__netflix='None').order_by('-rating_id__rating'))
    return get_category_movies(netflix_movies, request)


def top_movies(request):
    top_list = list(all_movies.order_by('-rating_id__rating')[:100])
    return get_category_movies(top_list, request)


def advanced_search(request):
    my_watchlist = get_watchlist(request)
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

            if get_cast:
                get_cast = difflib.get_close_matches(get_cast, all_cast)

                if len(get_cast) > 0: get_cast = get_cast[0]
                else: get_cast = 'No matches'
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

            if sorting == 'byYear':
                movie_items = list(all_movies.intersection(year).order_by('-release'))
            elif sorting == 'byVotes':
                movie_items = list(all_movies.intersection(rating, year, genres, cast, keywords).order_by('-votes'))
            else:
                movie_items = list(all_movies.intersection(rating, year, genres, cast, keywords).order_by('-rating_id__rating'))

        page = request.GET.get('page')
        paginator_advanced_search = Paginator(movie_items, 15)

        try:
            movie_items = paginator_advanced_search.page(page)
        except PageNotAnInteger:
            movie_items = paginator_advanced_search.page(1)
        except EmptyPage:
            movie_items = paginator_advanced_search.page(paginator_advanced_search.num_pages)

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

        page = request.GET.get('page')
        paginator_genre = Paginator(movie_items, 15)

        try:
            movie_items = paginator_genre.page(page)
        except PageNotAnInteger:
            movie_items = paginator_genre.page(1)
        except EmptyPage:
            movie_items = paginator_genre.page(paginator_genre.num_pages)

    return render(request, 'movie_finder/special-item.html', {'movieItems': movie_items, 'genreType': genre_type,
                                                              'myWatchlist': my_watchlist})


def show_intro(request):
    youtube = request.POST.get('intro', 'False')
    title = request.POST.get('title', 'False')

    if youtube != 'False' and title != 'False':
        imdb = all_movies.get(title=title)[0]
        return render(request, "movie_finder/intro.html", {'youtube': "https://www.youtube.com/watch?v=" + youtube, 'title': title,
                                              'imdb': imdb})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def result_page(request, movie_id: str):
    movie = request.POST.get('movie', False)
    intro = request.POST.get('intro', False)
    msg = request.POST.get('msg', False)
    if movie or movie_id:
        search = list(all_movies.get(imdb_id=movie_id))

        imdb_id = search[0].strip()
        title = search[1].strip()
        rating = int(float(str(search[2]).strip()) * 10)
        link = search[3].strip()
        votes = search[4]
        genres = search[5].strip()
        genres_split = genres.split(',')
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

        if msg:
            messages.success(request, msg)

        reviews = Review.objects.filter(movie=title)
        reviews_rate = False
        if reviews:
            reviews_rate = [(range(int(review.rating)), range(int(10 - review.rating))) for review in reviews]

        full_result = {'movie': movie, 'imdb_id': imdb_id, 'title': title, 'rating': rating, 'link': link,
                       'votes': votes, 'genres': genres, 'runtime': runtime, 'mtype': mType, 'netflix': mNetflix,
                       'plot': plot, 'poster': poster, 'genres_split': genres_split, 'year': year, 'youtube': youtube,
                       'cast_list': cast_list, 'reviews': reviews, 'reviews_rate': reviews_rate, 'intro': intro,
                       'msg': msg}

        return render(request, "movie_finder/result.html", full_result)
    else:
        messages.error(request, f'Error occurred while we\'re trying to show you info about the movie!')
        return redirect('/')


def movie_search(request):
    my_watchlist = get_watchlist(request)
    if request.GET:
        movie_items = False
        if ("q" in request.GET) and request.GET["q"].strip():
            query_title = request.GET["q"]
            found_movies = list(all_movies.filter(title__icontains=query_title).order_by('-rating_id__rating'))

            page = request.GET.get('page', 1)
            paginator_search = Paginator(found_movies, 10)

            try:
                movie_items = paginator_search.page(page)
            except PageNotAnInteger:
                movie_items = paginator_search.page(1)
            except EmptyPage:
                movie_items = paginator_search.page(paginator_search.num_pages)
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

    return render(request, "movie_finder/special-item.html", {'movieItems': popular_movies, 'myWatchlist': my_watchlist})
