from django.http import HttpResponse
from django.shortcuts import render
from .models import Recipe, Author


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
