from django.contrib import admin

from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):

    list_display = (
        "member_id",
        "full_name",
        "phone",
        "gender",
        "status",
        "join_date",
    )

    list_filter = (
        "status",
        "gender",
    )

    search_fields = (
        "member_id",
        "full_name",
        "phone",
        "email",
    )

    ordering = (
        "-created_at",
    )