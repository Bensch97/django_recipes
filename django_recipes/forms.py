from django import forms
from .models import Author


class AuthorForm(forms.Form):
    name = forms.CharField(label='Author name', max_length=50)
    bio = forms.CharField(label='Author bio', widget=forms.Textarea)


class RecipeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields['author'].choices = self.get_author_list()

    def get_author_list(self):
        author_list = [(a.id, a.name) for a in Author.objects.all()]
        return author_list

    title = forms.CharField(max_length=50)
    author = forms.ChoiceField(widget=forms.Select)
    description = forms.CharField(max_length=280)
    time_required = forms.CharField(max_length=50)
    instructions = forms.CharField(
        label='Recipe instructions',
        widget=forms.Textarea
    )
