from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Store, StoreInventory, StoreStaff
from .permissions import IsStoreAdminOrReadOnly, IsStoreStaffOrReadOnly
from .serializers import StoreInventorySerializer, StoreSerializer, StoreStaffSerializer


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all().prefetch_related("store_staff__user")
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated, IsStoreAdminOrReadOnly]

    def get_store(self):
        if self.action in ["list", "create"]:
            return None
        pk = self.kwargs.get(self.lookup_field or "pk")
        if not pk:
            return None
        return Store.objects.filter(pk=pk).first()


class StoreStaffViewSet(viewsets.ModelViewSet):
    queryset = StoreStaff.objects.select_related("store", "user").all()
    serializer_class = StoreStaffSerializer
    permission_classes = [IsAuthenticated, IsStoreAdminOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        store_id = self.request.query_params.get("store")
        if store_id:
            queryset = queryset.filter(store_id=store_id)
        return queryset

    def get_store(self):
        store_id = self.request.data.get("store") or self.request.query_params.get("store")
        if store_id:
            try:
                return Store.objects.get(pk=store_id)
            except Store.DoesNotExist:
                return None
        if self.action in ["retrieve", "update", "partial_update", "destroy"]:
            pk = self.kwargs.get(self.lookup_field or "pk")
            if pk:
                obj = StoreStaff.objects.select_related("store").filter(pk=pk).first()
                if obj:
                    return obj.store
        return None


class StoreInventoryViewSet(viewsets.ModelViewSet):
    queryset = StoreInventory.objects.select_related("store", "book").all()
    serializer_class = StoreInventorySerializer
    permission_classes = [IsAuthenticated, IsStoreStaffOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        store_id = self.request.query_params.get("store")
        if store_id:
            queryset = queryset.filter(store_id=store_id)
        return queryset

    def get_store(self):
        store_id = self.request.data.get("store") or self.request.query_params.get("store")
        if store_id:
            try:
                return Store.objects.get(pk=store_id)
            except Store.DoesNotExist:
                return None
        if self.action in ["retrieve", "update", "partial_update", "destroy"]:
            pk = self.kwargs.get(self.lookup_field or "pk")
            if pk:
                obj = StoreInventory.objects.select_related("store").filter(pk=pk).first()
                if obj:
                    return obj.store
        return None

