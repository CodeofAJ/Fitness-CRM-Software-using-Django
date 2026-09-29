from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path("", views.reports_dashboard, name="dashboard"),
    path(
        "members/",
        views.member_report,
        name="member_report",
    ),
    path(
        "members/pdf/",
        views.member_report_pdf,
        name="member_report_pdf",
    ),
    path(
        "memberships/",
        views.membership_report,
        name="membership_report",
    ),
    path(
        "memberships/pdf/",
        views.membership_report_pdf,
        name="membership_report_pdf",
    ),
    path(
        "attendance/",
        views.attendance_report,
        name="attendance_report",
    ),
    path(
        "attendance/pdf/",
        views.attendance_report_pdf,
        name="attendance_report_pdf",
    ),
    path(
        "trainers/",
        views.trainer_report,
        name="trainer_report",
    ),
    path(
        "trainers/pdf/",
        views.trainer_report_pdf,
        name="trainer_report_pdf",
    ),
    path(
        "combined/",
        views.combined_report,
        name="combined_report",
    ),
    path(
        "combined/pdf/",
        views.combined_report_pdf,
        name="combined_report_pdf",
    ),
]
