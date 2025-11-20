from django.urls import path

from .views import (
    BookListView,
    BookDetailView,
    GenreListView,
    AuthorListView,
)

urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    path('genres/', GenreListView.as_view(), name='genre-list'),
    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('<int:pk>/', BookDetailView.as_view(), name='book-detail'),
]
