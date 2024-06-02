from django import forms
from .models import Movie,List

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ["title", "year", "plot", "poster"]
        


class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ['name','is_public']