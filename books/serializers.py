from rest_framework import serializers
from .models import Book, Author, Genre

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'description']

class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    author_ids = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), many=True, write_only=True, source='authors')
    genre_ids = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True, write_only=True, source='genres')

    class Meta:
        model = Book
        fields = ['id', 'title', 'isbn', 'total_copies', 'available_copies', 'authors', 'genres', 'author_ids', 'genre_ids', 'created_by', 'cover_image']
        read_only_fields = ['available_copies', 'created_by']


