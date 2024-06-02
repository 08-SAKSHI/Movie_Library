from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from .models import Movie, List,MovieList
from .forms import MovieForm,ListForm
import requests
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save()
            return redirect("home")
    else:
        form = MovieForm()

    query = request.GET.get("query")
    if query:
        # Search movie on IMDB API
        api_key = "244cb2df"
        response = requests.get(f"http://www.omdbapi.com/?apikey={api_key}&t={query}")
        data = response.json()
        if data["Response"] == "True":
            movie_data = {
                "imdb_id": data["imdbID"],
                "year": data["Year"],
                "plot": data["Plot"],
                "poster": data["Poster"],
            }
        else:
            movie_data = None
    else:
        movie_data = None

    # Get user's movie lists
    user = request.user
    lists = List.objects.filter(user=user)

    # Get movies for each list
    list_movies = []
    for lst in lists:
        movies = MovieList.objects.filter(list=lst)
        list_movies.append((lst, movies))

    return render(request, "app/home.html", {
        "movie_data": movie_data,
        "list_movies": list_movies,
        "form": form,
    })

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'app/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out. Login in again.")
    return redirect('login')

def create_list(request):
    if request.method == 'POST':
        form = ListForm(request.POST)
        if form.is_valid():
            list_obj = form.save(commit=False)
            list_obj.user = request.user
            list_obj.save()
            return redirect('list')
    else:
        form = ListForm()
    return render(request, 'app/create_list.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def list(request):
    lists = List.objects.filter(user=request.user)
    return render(request, "app/list.html", {"lists": lists})

def movie_list(request, list_id):
    list_obj = List.objects.get(id=list_id)
    movies = MovieList.objects.filter(list=list_obj)
    return render(request, "app/list.html", {"list_obj": list_obj, "movies": movies})

def add_movie_to_list(request, list_id):
    list_obj = List.objects.get(id=list_id)
    movies = Movie.objects.all()
    if request.method == "POST":
        movie_id = request.POST.get("movie_id")
        movie = Movie.objects.get(id=movie_id)
        MovieList.objects.create(list=list_obj, movie=movie)
        return redirect("movie_list", list_id=list_id)
    return render(request, "app/add_movie_to_list.html", {"list_obj": list_obj, "movies": movies})


from django.http import HttpResponseForbidden
def film(request):
    if request.method == "POST":
        imdb_id = request.POST.get("imdb_id")
        movie, created = Movie.objects.get_or_create(imdb_id=imdb_id)
        if created:
            # Get movie data from IMDB API
            api_key = "244cb2df"
            response = requests.get(f"http://www.omdbapi.com/?apikey={api_key}&i={imdb_id}")
            data = response.json()
            movie.title = data["Title"]
            movie.year = data["Year"]
            movie.plot = data["Plot"]
            movie.poster = data["Poster"]
            movie.save()
        return redirect("home")
    return HttpResponseForbidden()