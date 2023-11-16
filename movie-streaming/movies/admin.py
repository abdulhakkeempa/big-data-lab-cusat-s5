from django.contrib import admin
from movies.models import Movie, Genre, UserMovieRating
from django.utils.html import format_html

# Register your models here.
admin.site.register(Genre)
admin.site.register(UserMovieRating)

class MovieAdmin(admin.ModelAdmin):
  search_fields = ['title']
  list_filter = ['language']

  list_display = ('id', 'title', 'description', 'length', 'release_year', 'language', 'image_display')
  ordering = ('id',)
  readonly_fields = ('added_date',)

  def image_display(self, obj):
      return format_html('<img src="{}" width="50" height="50" />', obj.poster)

  image_display.short_description = 'Image'

  def change_view(self, request, object_id, form_url='', extra_context=None):
      extra_context = extra_context or {}

      # Get the object
      obj = self.model.objects.get(pk=object_id)

      # Add the image to the extra context
      extra_context['image_display'] = format_html('<img src="{}" width="200" height="200" />', obj.poster)

      return super().change_view(
          request, object_id, form_url, extra_context=extra_context,
      )




admin.site.register(Movie, MovieAdmin)
