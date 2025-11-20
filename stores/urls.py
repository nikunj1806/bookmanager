from rest_framework.routers import DefaultRouter

from .views import StoreInventoryViewSet, StoreStaffViewSet, StoreViewSet

router = DefaultRouter()
router.register(r"stores", StoreViewSet, basename="store")
router.register(r"store-staff", StoreStaffViewSet, basename="store-staff")
router.register(r"store-inventory", StoreInventoryViewSet, basename="store-inventory")

urlpatterns = router.urls

