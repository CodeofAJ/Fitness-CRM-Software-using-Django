from celery import shared_task
from django.utils import timezone

from .models import Membership


@shared_task
def check_membership_expiry():

    today = timezone.localdate()

    expired_memberships = Membership.objects.filter(
        status="ACTIVE",
        end_date__lt=today
    )

    count = expired_memberships.update(
        status="EXPIRED"
    )

    return f"{count} membership(s) expired."