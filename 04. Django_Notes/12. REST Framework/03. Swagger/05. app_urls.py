from django.urls import path, include
from . import views, api
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

schema_view = get_schema_view(
    openapi.Info(
        title="Software Management API",
        default_version='v1',
        description="API documentation for Software Management",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()

# default router
router.register(r'software', api.SoftwareViewSet)

urlpatterns = [
    # Web Views (unchanged)

    # Modified verify_license 
    path('api/verify-license/<str:email>/<str:password>/<int:software_id>/<str:mac_address>/', 
         api.verify_license, 
         name='verify_license'),

    # API Router and Documentation
    path('api/', include(router.urls)),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
]

# Serve static files in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
