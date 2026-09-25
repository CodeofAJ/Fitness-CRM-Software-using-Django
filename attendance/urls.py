from django.urls import path

from . import views


app_name = "attendance"


urlpatterns = [
    path(
        "",
        views.attendance_dashboard,
        name="dashboard"
    ),

    path(
        "check-in/",
        views.attendance_check_in,
        name="check_in"
    ),

    path(
        "history/",
        views.attendance_history,
        name="history"
    ),

    path(
        "member/<str:member_id>/",
        views.member_attendance_history,
        name="member_history"
    ),

    path(
        "<int:pk>/check-out/",
        views.attendance_check_out,
        name="check_out"
    ),
]