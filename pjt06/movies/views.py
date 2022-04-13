from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_safe, require_POST,require_http_methods
from .models import Movie
from .forms import MovieForm


# Create your views here.
@require_safe
def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }

    return render(request, 'movies/index.html', context)

@require_http_methods(['POST','GET'])
def create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save()
            return redirect('movies:detail', movie.pk)
    else:
        form = MovieForm()

    context = {
        'form': form,

    }

    return render(request, 'movies/create.html', context)

@require_safe
def detail(request, movie_pk):
    # movie = Movie.objects.get(pk=movie_pk)
    movie = get_object_or_404(Movie, pk=movie_pk)
    context = {
        'movie' : movie,
    }

    return render(request,'movies/detail.html',context)


@require_http_methods(['POST','GET'])
def update(request,movie_pk):
    # movie = Movie.objects.get(pk=movie_pk)
    movie = get_object_or_404(Movie,pk=movie_pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            movie = form.save()
        return redirect('movies:detail',movie.pk)
    else:
        form = MovieForm(instance=movie)
    
    context ={
        'form' : form,
        'movie' : movie,
    }
    return render(request,'movies/update.html',context)


@require_POST
def delete(request,movie_pk):
    # movie = Movie.objects.get(pk=movie_pk)
    movie = get_object_or_404(Movie,pk=movie_pk)

    # if request.method == 'POST':/
    movie.delete()
    return redirect('movies:index')
    
    # return redirect('movies:detail', movie_pk)


