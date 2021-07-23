from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect

from django.shortcuts import render
from django.views.generic import (ListView,  UpdateView, DeleteView)

from .forms import ReviewForms
from .models import Review


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
            msg = f'Added review for "{movie_selected}"'
            form.save()
            return render(request, 'movie_finder/review.html', {'form': form, 'msg': msg, 'movie': movie_selected, 'imdb': imdb,
                                                   'back': True})
        else:
            print(form.errors)
    else:
        form = ReviewForms()

    params = {'form': form, 'movie': movie_selected, 'imdb': imdb, 'back': False}
    return render(request, 'movie_finder/review.html', params)


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
    success_url = '/reviews/'

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
    success_url = '/reviews/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author or self.request.user.is_superuser:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        messages.error(self.request, self.success_message)
        return super(PostDeleteView, self).delete(request, *args, **kwargs)
