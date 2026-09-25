from django.urls import path

from . import views

app_name = "payments"


urlpatterns = [
    path("", views.payment_list, name="list"),
    path("<int:pk>/", views.payment_detail, name="detail"),
    path(
        "member/<str:member_id>/", views.member_payment_history, name="member_history"
    ),
    path(
        "razorpay/<int:pk>/",
        views.razorpay_payment,
        name="razorpay_payment",
    ),
]
