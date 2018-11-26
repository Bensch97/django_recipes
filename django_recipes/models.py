from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=50)
    bio = models.TextField(max_length=280)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.CharField(max_length=280)
    time_required = models.CharField(max_length=50)
    instructions = models.TextField(max_length=280)

    def __str__(self):
        return self.title
