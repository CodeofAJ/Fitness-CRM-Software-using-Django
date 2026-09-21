from django.urls import path

from . import views

app_name = "memberships"


urlpatterns = [
    path("", views.plan_list, name="plan_list"),
    path("add/", views.plan_create, name="plan_create"),
    path("<int:pk>/edit/", views.plan_update, name="plan_update"),
    path(
        "<int:pk>/toggle-status/", views.plan_toggle_status, name="plan_toggle_status"
    ),
    # Memberships
    path("records/", views.membership_list, name="membership_list"),
    path("records/add/", views.membership_create, name="membership_create"),
    path("records/<int:pk>/", views.membership_detail, name="membership_detail"),
    path("records/<int:pk>/renew/", views.membership_renew, name="membership_renew"),
    path("history/<str:member_id>/", views.membership_history, name="membership_history"),
]
