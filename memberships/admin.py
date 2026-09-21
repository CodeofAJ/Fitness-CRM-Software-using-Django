from django.contrib import admin

from .models import Membership, MembershipPlan


@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "duration_months",
        "price",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "duration_months",
    )

    search_fields = (
        "name",
        "description",
    )

    ordering = (
        "duration_months",
        "price",
    )


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):

    list_display = (
        "member",
        "plan",
        "start_date",
        "end_date",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "plan",
        "start_date",
        "end_date",
    )

    search_fields = (
        "member__member_id",
        "member__full_name",
        "member__phone",
        "plan__name",
    )

    ordering = (
        "-created_at",
    )    