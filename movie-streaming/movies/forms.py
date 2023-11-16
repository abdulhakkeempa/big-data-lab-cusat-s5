from django import forms
from movies.models import Genre


class MovieChangeListForm(forms.ModelForm):

    # here we only need to define the field we want to be editable
    genre = forms.ModelMultipleChoiceField(queryset=Genre.objects.all(), 
        required=False)
