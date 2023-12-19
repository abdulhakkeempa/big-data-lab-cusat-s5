from django.urls import path, include
from movies.views import  ListMovies, MovieDetail, ListAllMovies
from .views import stream_video, salaar

urlpatterns = [
    path("", ListMovies.as_view(), name="movies"),
    path("movie/all", ListAllMovies.as_view(), name="all-movies"),
    path("movie/<int:pk>", MovieDetail.as_view(), name="movies-individual"),
    path('stream_video/', stream_video, name='stream_video'),
    path('salaar/', salaar, name='salaar'),
]