from django.contrib import admin
from movies.models import Movie, Genre, UserMovieRating
from movies.forms import MovieChangeListForm

# Register your models here.
admin.site.register(Genre)
admin.site.register(UserMovieRating)


class MovieAdmin(admin.ModelAdmin):
  search_fields = ['title']
  list_filter = ['language']

admin.site.register(Movie, MovieAdmin)
