from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=4)
    imdb_id = models.CharField(max_length=9, unique=True)
    plot = models.TextField()
    poster = models.URLField()

    def __str__(self):
        return self.title

class List(models.Model):
    name = models.CharField(max_length=255)
    is_public = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class MovieList(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    list = models.ForeignKey(List, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.movie.title} - {self.list.name}"