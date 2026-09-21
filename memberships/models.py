from django.db import models


class MembershipPlan(models.Model):

    DURATION_CHOICES = [
        (1, "1 Month"),
        (3, "3 Months"),
        (6, "6 Months"),
        (12, "12 Months"),
    ]

    name = models.CharField(
        max_length=100,
        unique=True
    )

    duration_months = models.PositiveIntegerField(
        choices=DURATION_CHOICES
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["duration_months", "price"]

    def __str__(self):
        return self.name



class Membership(models.Model):

    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("EXPIRED", "Expired"),
        ("CANCELLED", "Cancelled"),
        ("PENDING", "Pending"),
    ]

    member = models.ForeignKey(
        "members.Member",
        on_delete=models.PROTECT,
        related_name="memberships"
    )

    plan = models.ForeignKey(
        MembershipPlan,
        on_delete=models.PROTECT,
        related_name="memberships"
    )

    start_date = models.DateField()

    end_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
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
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.member.full_name} - "
            f"{self.plan.name}"
        )        