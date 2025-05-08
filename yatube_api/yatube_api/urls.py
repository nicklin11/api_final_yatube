from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.conf import settings  # For media files in development
from django.conf.urls.static import static  # For media files in development
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
