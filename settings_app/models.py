from django.db import models


class GymSettings(models.Model):
    gym_name = models.CharField(
        max_length=150,
        default="GMS Gym",
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    website = models.URLField(
        blank=True,
    )

    address = models.TextField(
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "Gym Settings"
        verbose_name_plural = "Gym Settings"

    def __str__(self):
        return self.gym_name