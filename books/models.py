from django.db import models
from django.utils import timezone
from users.models import User

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=300)
    authors = models.ManyToManyField(Author, related_name='books')
    isbn = models.CharField(max_length=13, unique=True)
    genres = models.ManyToManyField(Genre, related_name='books', blank=True)
    total_copies = models.PositiveIntegerField(default=100)
    available_copies = models.PositiveIntegerField(default=100)
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title
