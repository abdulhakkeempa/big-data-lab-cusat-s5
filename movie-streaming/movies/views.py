from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from movies.models import Movie, UserMovieRating
from django.contrib.auth.mixins import LoginRequiredMixin
from movies.recommendations import get_item_based_recommendation, get_content_based_recommendations
import re

# Function to remove year from movie title
def remove_year(movies):
    # Define a regex pattern to match the parentheses and the year inside
    pattern = re.compile(r'\s*\([^)]*\)\s*')

    # Use the pattern to replace the matched substring with an empty string
    movies_cleaned = [pattern.sub('', s) for s in movies]
    return movies_cleaned


class ListMovies(LoginRequiredMixin, ListView):
  model = Movie
  context_object_name = 'movies'
  template_name = 'movies/movies.html'
  login_url = '/login'

  def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
    context = super().get_context_data(**kwargs)

    # Get the current user
    user = self.request.user

    context['movies'] = Movie.objects.all()[:25] # get the first 25 movies
    context['continue_watching'] = Movie.objects.filter(usermovierating__user=user) # where the users have provided a rating
    context['content_recommended'] = self.recommend_movies() # get the content based recommendations
    context['item_recommended'] = self.suggest_movies() # get the collaborative item-item based recommendations
    return context

  def recommend_movies(self, **kwargs):
      movies = self.get_user_watched_movies(5)
      if movies:
        movie_titles = [movie.title for movie in movies]
        recommended_movies = get_content_based_recommendations(movie_titles)
        # remove the year from the movie title
        cleaned_data = remove_year(recommended_movies[0])
        recommended_movies = Movie.objects.filter(title__in=cleaned_data)
        return recommended_movies
      
  def suggest_movies(self, **kwargs):
    movies = self.get_user_watched_movies(5)
    if movies:
      suggested_movies = []
      group = {}
      for movie in movies:
        recommended_movies = get_item_based_recommendation(movie.title)
        # remove the year from the movie title
        cleaned_data = remove_year(recommended_movies)
        similar_movies = Movie.objects.filter(title__in=cleaned_data)
        if similar_movies:
          group[f'{movie.title}'] = similar_movies
      
      suggested_movies.append(group)
      return suggested_movies

  def get_user_watched_movies(self, n_watched=5,**kwargs):
    """
      Returns the latest 5 movies the user has watched

      Args:
        n_watched (int): The number of movies to be returned

      Returns:
        list: A list of Movie objects
    """
    user = self.request.user
    return Movie.objects.filter(usermovierating__user=user)[:n_watched]
  
class MovieDetail(LoginRequiredMixin, View):
  login_url = '/login'

  def get(self, request, pk):
    movie = Movie.objects.get(pk=pk)
    rating = int(abs(movie.get_review_values))
    rating_list = [True if i < rating else False for i in range(5)]

    #fetching the rating providied by the user
    try:
      user_rating = UserMovieRating.objects.get(user=request.user, movie=movie)
      user_rating = user_rating.rating
    except UserMovieRating.DoesNotExist:
      user_rating = 0

    return render(request, 'movies/movies-individual.html', {'movie': movie, 'global_rating_list': rating_list, 'user_rating': user_rating})
  
  def post(self, request, pk):
    movie = Movie.objects.get(pk=pk)
    user = request.user
    rating = request.POST.get('review')

    if UserMovieRating.objects.filter(user=user, movie=movie).exists():
      user_movie_rating  = UserMovieRating.objects.get(user=user, movie=movie)
      user_movie_rating.rating = rating
      user_movie_rating.save()
      return redirect('movies-individual', pk=pk)

    user_movie_rating = UserMovieRating(user=user, movie=movie, rating=rating)
    user_movie_rating .save()
    return redirect('movies-individual', pk=pk)

class ListAllMovies(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Movie      
    context_object_name = 'movies'
    template_name = 'movies/movies-all.html'
    paginate_by = 20  
