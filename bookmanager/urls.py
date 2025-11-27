from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

from users.views import CurrentUserView, MemberRegistrationView, MemberProfileUpdateView

schema_view = get_schema_view(
    openapi.Info(
        title="Books Management API",
        default_version="v1",
        description="API documentation for Book Manager System (Books, Loans, Payments, Users)",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@bookmanager.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls")),

    # JWT auth endpoints
    path('api/auth/token/', TokenObtainPairView.as_view(), name='auth_token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='auth_token_refresh'),
    path('api/auth/token/logout/', TokenBlacklistView.as_view(), name='auth_token_logout'),
    path('api/auth/me/', CurrentUserView.as_view(), name='auth_me'),
    path('api/auth/register/', MemberRegistrationView.as_view(), name='auth_register'),
    path('api/profile/update/', MemberProfileUpdateView.as_view(), name='member-profile-update'),
    
    path("api/books/", include("books.urls")),
    path("api/borrow/", include("loans.urls")),
    path("api/payment/", include("payments.urls")),
    path("api/membership/", include("payments.membership_urls")),
    path("api/purchase/", include("payments.purchase_urls")),
    # path("api/", include("stores.urls")),

    # Swagger / ReDoc
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)