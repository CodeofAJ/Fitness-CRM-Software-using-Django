from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

from members.views import dashboard
from memberships.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    # Authentication
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path("", dashboard, name="dashboard"),
    path("members/", include("members.urls")),
    path("memberships/", include("memberships.urls")),
    path("payments/", include("payments.urls")),
    path("attendance/", include("attendance.urls")),
    path("trainers/", include("trainers.urls")),
    path("reports/", include("reports.urls")),
    path("settings/", include("settings_app.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
