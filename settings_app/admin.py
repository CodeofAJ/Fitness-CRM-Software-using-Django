from django.contrib import admin
from .models import GymSettings


@admin.register(GymSettings)
class GymSettingsAdmin(admin.ModelAdmin):

    list_display = (
        "gym_name",
        "phone",
        "email",
        "updated_at",
    )

    readonly_fields = (
        "updated_at",
    )