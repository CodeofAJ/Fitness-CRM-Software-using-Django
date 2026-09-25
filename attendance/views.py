from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from members.models import Member

from .forms import AttendanceCheckInForm
from .models import Attendance


@login_required
def attendance_dashboard(request):

    today = timezone.localdate()

    attendance_records = (
        Attendance.objects
        .select_related("member")
        .filter(date=today)
        .order_by("-check_in", "member__full_name")
    )

    # Today's statistics
    total_attendance = attendance_records.count()

    currently_inside = attendance_records.filter(
        check_in__isnull=False,
        check_out__isnull=True,
    ).count()

    checked_out = attendance_records.filter(
        check_out__isnull=False,
    ).count()

    active_members = Member.objects.filter(
        status="ACTIVE"
    ).count()

    not_checked_in = max(
        active_members - total_attendance,
        0
    )

    # Today's attendance percentage
    if active_members > 0:
        attendance_rate = round(
            (total_attendance / active_members) * 100,
            1
        )
    else:
        attendance_rate = 0

    # Last 7 days
    seven_days_ago = today - timedelta(days=6)  

    weekly_attendance = Attendance.objects.filter(
        date__range=[
            seven_days_ago,
            today,
        ]
    ).count()

    context = {
        "attendance_records": attendance_records,

        "total_attendance": total_attendance,
        "currently_inside": currently_inside,
        "checked_out": checked_out,
        "not_checked_in": not_checked_in,

        "active_members": active_members,
        "attendance_rate": attendance_rate,
        "weekly_attendance": weekly_attendance,

        "today": today,
    }

    return render(
        request,
        "attendance/dashboard.html",
        context
    )


@login_required
def attendance_check_in(request):

    if request.method == "POST":

        form = AttendanceCheckInForm(request.POST)

        if form.is_valid():

            member = form.cleaned_data["member"]

            # Safety check in case the member's status
            # changed after the form was displayed.
            if member.status != "ACTIVE":

                messages.error(
                    request, f"{member.full_name} is inactive and cannot check in."
                )

                return redirect("attendance:dashboard")

            today = timezone.localdate()
            current_time = timezone.localtime().time()

            attendance, created = Attendance.objects.get_or_create(
                member=member,
                date=today,
                defaults={
                    "check_in": current_time,
                    "status": "PRESENT",
                },
            )

            if not created:

                if attendance.check_in:

                    messages.warning(
                        request, f"{member.full_name} is already checked in today."
                    )

                else:

                    attendance.check_in = current_time
                    attendance.status = "PRESENT"

                    attendance.save(
                        update_fields=[
                            "check_in",
                            "status",
                            "updated_at",
                        ]
                    )

                    messages.success(
                        request, f"{member.full_name} checked in successfully."
                    )

            else:

                messages.success(
                    request, f"{member.full_name} checked in successfully."
                )

            return redirect("attendance:dashboard")

    else:

        form = AttendanceCheckInForm()

    return render(
        request,
        "attendance/check_in.html",
        {
            "form": form,
        },
    )


@login_required
def attendance_check_out(request, pk):

    attendance = get_object_or_404(Attendance.objects.select_related("member"), pk=pk)

    if attendance.check_out:

        messages.warning(
            request, f"{attendance.member.full_name} is already checked out."
        )

    else:

        attendance.check_out = timezone.localtime().time()

        attendance.save(
            update_fields=[
                "check_out",
                "updated_at",
            ]
        )

        messages.success(
            request, f"{attendance.member.full_name} checked out successfully."
        )

    return redirect("attendance:dashboard")


@login_required
def attendance_history(request):

    search = request.GET.get("search", "").strip()

    date = request.GET.get("date", "").strip()

    attendance_records = Attendance.objects.select_related("member").all()

    if search:
        attendance_records = attendance_records.filter(
            Q(member__member_id__icontains=search)
            | Q(member__full_name__icontains=search)
            | Q(member__phone__icontains=search)
        )

    if date:
        try:
            selected_date = datetime.strptime(date, "%Y-%m-%d").date()

            attendance_records = attendance_records.filter(date=selected_date)

        except ValueError:
            date = ""

    paginator = Paginator(attendance_records, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "attendance/history.html",
        {
            "page_obj": page_obj,
            "attendance_records": page_obj.object_list,
            "search": search,
            "date": date,
        },
    )


@login_required
def member_attendance_history(request, member_id):

    member = get_object_or_404(Member, member_id=member_id)

    attendance_records = Attendance.objects.filter(member=member).order_by(
        "-date", "-check_in"
    )

    paginator = Paginator(attendance_records, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "attendance/member_history.html",
        {
            "member": member,
            "page_obj": page_obj,
            "attendance_records": page_obj.object_list,
        },
    )


@login_required
def attendance_dashboard(request):

    today = timezone.localdate()

    attendance_records = (
        Attendance.objects.select_related("member")
        .filter(date=today)
        .order_by("-check_in", "member__full_name")
    )

    total_attendance = attendance_records.count()

    currently_inside = attendance_records.filter(
        check_in__isnull=False,
        check_out__isnull=True,
    ).count()

    checked_out = attendance_records.filter(
        check_out__isnull=False,
    ).count()

    active_members = Member.objects.filter(status="ACTIVE").count()

    not_checked_in = max(active_members - total_attendance, 0)

    context = {
        "attendance_records": attendance_records,
        "total_attendance": total_attendance,
        "currently_inside": currently_inside,
        "checked_out": checked_out,
        "not_checked_in": not_checked_in,
        "today": today,
    }

    return render(request, "attendance/dashboard.html", context)
