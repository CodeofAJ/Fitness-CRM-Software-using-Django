from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from members.views import test_ui


urlpatterns = [
    path('admin/', admin.site.urls),
    path("test-ui/", test_ui, name="test-ui"),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
