from django.urls import path, include
from movies.views import  ListMovies, MovieDetail, ListAllMovies

urlpatterns = [
    path("", ListMovies.as_view(), name="movies"),
    path("all", ListAllMovies.as_view(), name="all-movies"),
    path("<int:pk>", MovieDetail.as_view(), name="movies-individual"),
]