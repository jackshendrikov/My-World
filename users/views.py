from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect, HttpResponse

from django.shortcuts import render, redirect
from django.views.generic import (ListView,  UpdateView, DeleteView)

from movie_finder.models import Movie
from .forms import ReviewForms
from .models import Review, MyRating


@login_required
def fill_form(request):
    movie_selected = request.GET.get('movie', 'notSelected')
    imdb = request.GET.get('imdb', 'notSelected')
    if movie_selected == 'notSelected' or imdb == 'notSelected':
        messages.warning(request, f'URL Not Allowed. Select the movie first!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if request.method == 'POST':
        form = ReviewForms(request.POST or None)
        if form.is_valid():
            form.instance.author = request.user
            form.instance.movie = movie_selected
            form.instance.imdb = imdb
            form.save()

            messages.success(request, f'Added review for "{movie_selected}"')
            return redirect('movie-finder:result', imdb)
        else:
            print(form.errors)
    else:
        form = ReviewForms()

    params = {'form': form, 'movie': movie_selected, 'imdb': imdb}
    return render(request, 'movie_finder/review.html', params)


@login_required
def add_rating(request):
    if request.method == 'POST':
        imdb = request.POST.get('imdb')
        rating = request.POST.get('rating')

        movie = Movie.objects.get(imdb_id=imdb)

        if MyRating.objects.filter(movie=movie, user=request.user).exists():
            MyRating.objects.filter(movie=movie, user=request.user).update(rating=rating)
            return HttpResponse(status=204)
        else:
            MyRating(movie=movie, user=request.user, rating=rating).save()
            return HttpResponse(status=204)

    return redirect(request.META['HTTP_REFERER'])


class PostListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'movie_finder/all-reviews.html'
    context_object_name = 'reviewPosts'
    ordering = ['-timestamp']
    paginate_by = 10


class PostListViewUser(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'movie_finder/my-reviews.html'
    context_object_name = 'reviewPosts'
    ordering = ['-timestamp']


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    context_object_name = 'reviews'
    fields = ['rating', 'review_description']
    template_name = 'movie_finder/review.html'
    success_url = '/movie-finder/reviews/'

    def form_valid(self, form, *args, **kwargs):
        form.instance.author = self.request.user
        messages.add_message(self.request, messages.INFO, f'Your review has been updated!')
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'movie_finder/confirm-delete.html'
    success_message = f"Review has been deleted successfully."
    success_url = '/movie-finder/reviews/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author or self.request.user.is_superuser:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        messages.error(self.request, self.success_message)
        return super(PostDeleteView, self).delete(request, *args, **kwargs)
