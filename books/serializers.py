from django.db.models import Sum, Min
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
    
    # Aggregated inventory fields from all stores
    total_copies = serializers.SerializerMethodField()
    available_copies = serializers.SerializerMethodField()
    copies_for_sale = serializers.SerializerMethodField()
    sale_price = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'isbn',
            'authors',
            'genres',
            'author_ids',
            'genre_ids',
            'created_by',
            'cover_image',
            'total_copies',
            'available_copies',
            'copies_for_sale',
            'sale_price',
        ]
        read_only_fields = ['created_by', 'total_copies', 'available_copies', 'copies_for_sale', 'sale_price']

    def get_total_copies(self, obj):
        """Sum of total_copies across all stores for this book."""
        from stores.models import StoreInventory
        result = StoreInventory.objects.filter(book=obj).aggregate(
            total=Sum('total_copies')
        )
        return result['total'] or 0

    def get_available_copies(self, obj):
        """Sum of available_copies across all stores for this book."""
        from stores.models import StoreInventory
        result = StoreInventory.objects.filter(book=obj).aggregate(
            total=Sum('available_copies')
        )
        return result['total'] or 0

    def get_copies_for_sale(self, obj):
        """Sum of copies_for_sale across all stores where applied_for_sale is True."""
        from stores.models import StoreInventory
        result = StoreInventory.objects.filter(
            book=obj,
            applied_for_sale=True,
            copies_for_sale__gt=0
        ).aggregate(
            total=Sum('copies_for_sale')
        )
        return result['total'] or 0

    def get_sale_price(self, obj):
        """Minimum sale_price among stores where copies_for_sale > 0."""
        from stores.models import StoreInventory
        result = StoreInventory.objects.filter(
            book=obj,
            applied_for_sale=True,
            copies_for_sale__gt=0,
            sale_price__isnull=False
        ).aggregate(
            min_price=Min('sale_price')
        )
        return float(result['min_price']) if result['min_price'] else None


