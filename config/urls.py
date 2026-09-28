from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from members.views import dashboard
from memberships.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", dashboard, name="dashboard"),
    path("members/", include("members.urls")),
    path("memberships/", include("memberships.urls")),
    path("payments/", include("payments.urls")),
    path("attendance/", include("attendance.urls")),
    path("trainers/", include("trainers.urls")),
    path("reports/", include("reports.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
