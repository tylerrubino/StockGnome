from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from main.views import index

urlpatterns = [
    path('admin/', admin.site.urls),

    # Base API Endpoint
    path('api/v1/', include('api.urls')),
] + static(settings.STATIC_URL  , document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),