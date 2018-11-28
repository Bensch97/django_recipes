from django.http import HttpResponse
from django.shortcuts import render

from .models import Recipe, Author
from .forms import AuthorForm, RecipeForm


def current_recipes(request):
    data = Recipe.objects.all()
    return render(request, 'recipes.html', {'data': data})


def recipe_details(request, recipe_id):
    data = Recipe.objects.get(pk=recipe_id)
    return render(request, 'recipe-details.html', {'data': [data]})


def author_details(request, author_id):

    data = {
        'author': Author.objects.get(pk=author_id),
        'recipes': list(Recipe.objects.all().filter(
            author__id=author_id).values()
        )
    }
    return render(request, 'author-details.html', {'data': data})


def recipe_add(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data['title'],
                author=Author.objects.filter(id=data['author']).first(),
                description=data['description'],
                time_required=data['time_required'],
                instructions=data['instructions'],
            )
            return render(request, 'thanks.html')
    else:
        form = RecipeForm()
    return render(request, 'recipe-form.html', {'form': form})


def author_add(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Author.objects.create(
                name=data['name'],
                bio=data['bio'],
            )
            return render(request, 'thanks.html')
    else:
        form = AuthorForm()

    return render(request, 'author-form.html', {'form': form})
