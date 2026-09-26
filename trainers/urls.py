from django.urls import path

from . import views


app_name = "trainers"


urlpatterns = [

    path(
        "",
        views.trainer_list,
        name="list"
    ),

    path(
        "add/",
        views.trainer_create,
        name="create"
    ),

    path(
        "<str:trainer_id>/",
        views.trainer_detail,
        name="detail"
    ),

    path(
        "<str:trainer_id>/edit/",
        views.trainer_update,
        name="update"
    ),

    path(
        "<str:trainer_id>/toggle-status/",
        views.trainer_toggle_status,
        name="toggle_status"
    ),
]