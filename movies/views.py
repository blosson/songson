from django.shortcuts import render, redirect
from django.views.decorators.http import require_safe
from .models import Movie, Genre
from random import randint

# Create your views here.
@require_safe
def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)

@require_safe
def detail(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    # genre = movie.genres.all()
    context = {
        'movie': movie,
        # 'genre': genre,
    }
    return render(request, 'movies/detail.html', context)

@require_safe
def recommended(request):
    user = request.user
    movies = Movie.objects.all()
    if user.is_authenticated:
        random_num = []
        for _ in range(30):
            random_num.append(randint(1, 201))
        movie_list = []
        for i in random_num:
            for movie in movies:
                if i == movie.pk:
                    movie_list.append(movie)
        sort_key = lambda x:x.vote_average
        movie_list = sorted(movie_list, key=sort_key)[30:20:-1]
        # movie_list = movie_list.order_by('-vote_average')[:10]
        context = {
            'movie_list': movie_list,
        }
        return render(request, 'movies/recommended.html', context)
