from django.db import models

from members.models import Member


class Attendance(models.Model):

    STATUS_CHOICES = [
        ("PRESENT", "Present"),
        ("ABSENT", "Absent"),
    ]

    member = models.ForeignKey(
        Member,
        on_delete=models.PROTECT,
        related_name="attendance_records"
    )

    date = models.DateField()

    check_in = models.TimeField(
        blank=True,
        null=True
    )

    check_out = models.TimeField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PRESENT"
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-date", "-check_in"]

        constraints = [
            models.UniqueConstraint(
                fields=["member", "date"],
                name="unique_member_attendance_per_day"
            )
        ]

    def __str__(self):
        return f"{self.member.full_name} - {self.date}"