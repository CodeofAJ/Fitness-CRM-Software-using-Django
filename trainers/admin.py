from django.contrib import admin

from .models import Trainer


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):

    list_display = (
        "trainer_id",
        "full_name",
        "specialization",
        "experience_years",
        "phone",
        "status",
        "joining_date",
    )

    list_filter = (
        "status",
        "gender",
        "specialization",
        "joining_date",
    )

    search_fields = (
        "trainer_id",
        "full_name",
        "phone",
        "email",
        "specialization",
    )

    ordering = (
        "-created_at",
    )