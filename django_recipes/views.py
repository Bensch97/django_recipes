from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from .models import Recipe, Author
from .forms import AuthorForm, RecipeForm, LoginForm, SignupForm


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


@login_required()
def recipe_add(request):
    if request.method == 'POST':
        form = RecipeForm(request.user, request.POST)
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
        form = RecipeForm(user=request.user)
    return render(request, 'recipe-form.html', {'form': form})


@staff_member_required()
def author_add(request):
    form = AuthorForm(None or request.POST)
    if form.is_valid():
        data = form.cleaned_data
        Author.objects.create(
            name=data['name'],
            bio=data['bio'],
        )
        return render(request, 'thanks.html')
    return render(request, 'author-form.html', {'form': form})


def signup_user(request):
    form = SignupForm(None or request.POST)

    if form.is_valid():
        data = form.cleaned_data
        user = User.objects.create_user(
            data['username'],
            data['email'],
            data['password']
        )
        login(request, user)
        return HttpResponseRedirect(reverse('homepage'))
    return render(request, 'signup.html', {'form': form})


def login_user(request):
    next_page = request.GET.get('next')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'],
                password=data['password']
            )
            if user is not None:
                login(request, user)
                if next_page:
                    return HttpResponseRedirect(next_page)
                else:
                    return HttpResponseRedirect(reverse('homepage'))
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form, 'next': next_page})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))
