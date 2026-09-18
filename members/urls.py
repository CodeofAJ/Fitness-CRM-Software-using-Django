from django.urls import path

from . import views

app_name = "members"


urlpatterns = [
    path("", views.member_list, name="list"),
    path("add/", views.member_create, name="create"),
    path("<str:member_id>/", views.member_detail, name="detail"),
    path("<str:member_id>/edit/", views.member_update, name="update"),
    path(
        "<str:member_id>/toggle-status/",
        views.member_toggle_status,
        name="toggle_status",
    ),
]
