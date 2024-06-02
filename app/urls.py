from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='app/login.html',next_page='home'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("signup/", views.signup, name="signup"),
    path("home/", views.home, name="home"),
    path("list/", views.list, name="list"),
    path("list/<int:list_id>/", views.movie_list, name="movie_list"),
    path("create_list/", views.create_list, name="create_list"),
    path("list/<int:list_id>/add_movie/", views.add_movie_to_list, name="add_movie_to_list"),
    path('film/', views.film, name='film')
]