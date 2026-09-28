from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from attendance.models import Attendance
from members.models import Member
from memberships.models import Membership
from trainers.models import Trainer


@login_required
def reports_dashboard(request):
    total_members = Member.objects.count()
    active_members = Member.objects.filter(status="ACTIVE").count()
    inactive_members = Member.objects.filter(status="INACTIVE").count()

    total_memberships = Membership.objects.count()
    active_memberships = Membership.objects.filter(status="ACTIVE").count()
    expired_memberships = Membership.objects.filter(status="EXPIRED").count()

    total_attendance = Attendance.objects.count()
    total_trainers = Trainer.objects.count()
    active_trainers = Trainer.objects.filter(status="ACTIVE").count()

    context = {
        "total_members": total_members,
        "active_members": active_members,
        "inactive_members": inactive_members,
        "total_memberships": total_memberships,
        "active_memberships": active_memberships,
        "expired_memberships": expired_memberships,
        "total_attendance": total_attendance,
        "total_trainers": total_trainers,
        "active_trainers": active_trainers,
    }

    return render(request, "reports/dashboard.html", context)


@login_required
def member_report(request):

    members = Member.objects.all()

    # ---------------------------------------------------------
    # SEARCH
    # ---------------------------------------------------------

    search_query = request.GET.get("q", "").strip()

    if search_query:
        members = members.filter(
            Q(full_name__icontains=search_query)
            | Q(member_id__icontains=search_query)
            | Q(phone__icontains=search_query)
            | Q(email__icontains=search_query)
        )

    # ---------------------------------------------------------
    # STATUS FILTER
    # ---------------------------------------------------------

    status_filter = request.GET.get("status", "").strip()

    if status_filter in ["ACTIVE", "INACTIVE"]:
        members = members.filter(status=status_filter)

    # ---------------------------------------------------------
    # GENDER FILTER
    # ---------------------------------------------------------

    gender_filter = request.GET.get("gender", "").strip()

    valid_genders = [choice[0] for choice in Member.GENDER_CHOICES]

    if gender_filter in valid_genders:
        members = members.filter(gender=gender_filter)

    # ---------------------------------------------------------
    # DATE RANGE FILTER
    # ---------------------------------------------------------

    date_from = request.GET.get("date_from", "").strip()
    date_to = request.GET.get("date_to", "").strip()

    if date_from:
        try:
            parsed_date_from = datetime.strptime(date_from, "%Y-%m-%d").date()

            members = members.filter(join_date__gte=parsed_date_from)
        except ValueError:
            date_from = ""

    if date_to:
        try:
            parsed_date_to = datetime.strptime(date_to, "%Y-%m-%d").date()

            members = members.filter(join_date__lte=parsed_date_to)
        except ValueError:
            date_to = ""

    # ---------------------------------------------------------
    # REPORT STATISTICS
    # ---------------------------------------------------------

    total_members = members.count()
    active_members = members.filter(status="ACTIVE").count()
    inactive_members = members.filter(status="INACTIVE").count()

    male_members = members.filter(gender="MALE").count()
    female_members = members.filter(gender="FEMALE").count()
    other_members = members.exclude(gender__in=["MALE", "FEMALE"]).count()

    # ---------------------------------------------------------
    # PAGINATION
    # ---------------------------------------------------------

    paginator = Paginator(members.order_by("-join_date"), 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {
        "members": page_obj,
        "page_obj": page_obj,
        "total_members": total_members,
        "active_members": active_members,
        "inactive_members": inactive_members,
        "male_members": male_members,
        "female_members": female_members,
        "other_members": other_members,
        "search_query": search_query,
        "status_filter": status_filter,
        "gender_filter": gender_filter,
        "date_from": date_from,
        "date_to": date_to,
    }

    return render(
        request,
        "reports/member_report.html",
        context,
    )
