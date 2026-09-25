from django.contrib import admin

from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    list_display = (
        "member",
        "date",
        "check_in",
        "check_out",
        "status",
    )

    list_filter = (
        "status",
        "date",
    )

    search_fields = (
        "member__member_id",
        "member__full_name",
        "member__phone",
    )

    ordering = (
        "-date",
        "-check_in",
    )