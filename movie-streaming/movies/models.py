from django.db import models
from accounts.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Movie(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(null=False, max_length=1000)
    length = models.IntegerField(null=False)
    release_year = models.IntegerField(null=False)
    genres = models.ManyToManyField(Genre)
    language = models.CharField(max_length=100, null=False)
    poster = models.URLField(null=False)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_genres(self):
        return self.genres.all()
    
    def get_reviews(self):
        return self.usermovierating_set.all()
    
    @property
    def genres_names(self):
        return [genre.name for genre in self.get_genres()]

    @property
    def get_review_values(self):
        reviews = self.get_reviews()
        ratings = [review.rating for review in reviews]
        try:
            ratings = sum(ratings)/len(ratings)
        except ZeroDivisionError:
            ratings = 0

        return ratings
    

class UserMovieRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(
        default=0,
        null=False,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
    )

    def __str__(self) -> str:
        return self.user.first_name + ' - ' + self.movie.title
