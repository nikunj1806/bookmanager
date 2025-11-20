from rest_framework import generics

from .models import Book, Author, Genre
from .serializers import BookSerializer, AuthorSerializer, GenreSerializer


class BookListView(generics.ListCreateAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all().prefetch_related("authors", "genres")
        genre_id = self.request.query_params.get("genre") or self.request.query_params.get("genre_id")
        author_id = self.request.query_params.get("author") or self.request.query_params.get("author_id")
        if genre_id:
            queryset = queryset.filter(genres__id=genre_id)
        if author_id:
            queryset = queryset.filter(authors__id=author_id)
        return queryset.distinct()


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.all().prefetch_related("authors", "genres", "store_inventories")


class GenreListView(generics.ListAPIView):
    queryset = Genre.objects.all().order_by("name")
    serializer_class = GenreSerializer


class AuthorListView(generics.ListAPIView):
    queryset = Author.objects.all().order_by("name")
    serializer_class = AuthorSerializer
