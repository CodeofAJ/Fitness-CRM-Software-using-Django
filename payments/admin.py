from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "member",
        "membership",
        "amount",
        "payment_method",
        "status",
        "razorpay_order_id",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_method",
        "created_at",
    )

    search_fields = (
        "member__member_id",
        "member__full_name",
        "member__phone",
        "razorpay_order_id",
        "razorpay_payment_id",
    )

    ordering = (
        "-created_at",
    )