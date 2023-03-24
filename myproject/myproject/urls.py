from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title='DRF-Custom API',
        default_version='v1.0.0',
        description='Custom Template for Django Rest Framework for ML purpose.',
        contact=openapi.Contact(email="benny.serra@neuralgt.com"),
        url='https://www.mydomain.com/'
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

admin.site.site_header = 'DRF-Custom-ML Administration'
admin.site.site_title = 'DRF-Custom-ML Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/', include('myapp.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()