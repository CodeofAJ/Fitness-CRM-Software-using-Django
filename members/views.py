from datetime import timedelta  

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils import timezone

from attendance.models import Attendance
from memberships.models import Membership
from trainers.models import Trainer


from .forms import MemberForm
from .models import Member



@login_required
def dashboard(request):

    today = timezone.localdate()

    # -------------------------
    # Member Statistics
    # -------------------------
    total_members = Member.objects.count()

    active_members = Member.objects.filter(
        status="ACTIVE"
    ).count()

    inactive_members = Member.objects.filter(
        status="INACTIVE"
    ).count()

    # -------------------------
    # Trainer Statistics
    # -------------------------
    total_trainers = Trainer.objects.count()

    active_trainers = Trainer.objects.filter(
        status="ACTIVE"
    ).count()

    inactive_trainers = Trainer.objects.filter(
        status="INACTIVE"
    ).count()

    # -------------------------
    # Membership Statistics
    # -------------------------
    total_memberships = Membership.objects.count()

    active_memberships = Membership.objects.filter(
        status="ACTIVE"
    ).count()

    expired_memberships = Membership.objects.filter(
        status="EXPIRED"
    ).count()

    # -------------------------
    # Today's Attendance
    # -------------------------
    today_attendance = Attendance.objects.filter(
        date=today
    ).count()

    today_present = Attendance.objects.filter(
        date=today,
        status="PRESENT"
    ).count()

    today_absent = Attendance.objects.filter(
        date=today,
        status="ABSENT"
    ).count()

    # -------------------------
    # Last 7 Days Attendance
    # -------------------------
    attendance_labels = []
    attendance_data = []

    for days_ago in range(6, -1, -1):

        current_date = today - timedelta(days=days_ago)

        attendance_count = Attendance.objects.filter(
            date=current_date,
            status="PRESENT"
        ).count()

        attendance_labels.append(
            current_date.strftime("%a")
        )

        attendance_data.append(
            attendance_count
        )

    # -------------------------
    # Recent Members
    # -------------------------
    recent_members = Member.objects.order_by(
        "-created_at"
    )[:5]

    # -------------------------
    # Membership Expiry Alerts
    # -------------------------
    upcoming_expiry_date = today + timedelta(days=7)

    expiring_memberships = Membership.objects.filter(
    end_date__gte=today,
    end_date__lte=upcoming_expiry_date,
    status="ACTIVE",
    ).select_related(
        "member",
        "plan",
    ).order_by(
        "end_date"
    )[:5]

    # -------------------------
    # Dashboard Context
    # -------------------------
    context = {
        # Members
        "total_members": total_members,
        "active_members": active_members,
        "inactive_members": inactive_members,

        # Trainers
        "total_trainers": total_trainers,
        "active_trainers": active_trainers,
        "inactive_trainers": inactive_trainers,

        # Memberships
        "total_memberships": total_memberships,
        "active_memberships": active_memberships,
        "expired_memberships": expired_memberships,

        # Attendance
        "today_attendance": today_attendance,
        "today_present": today_present,
        "today_absent": today_absent,

        # Chart data
        "attendance_labels": attendance_labels,
        "attendance_data": attendance_data,

        # Recent data
        "recent_members": recent_members,
        "expiring_memberships": expiring_memberships,
    }

    return render(
        request,
        "dashboard/index.html",
        context
    )


@login_required
def member_list(request):

    search = request.GET.get("search", "").strip()
    status = request.GET.get("status", "").strip()

    members = Member.objects.all()

    # Search
    if search:
        members = members.filter(
            Q(member_id__icontains=search)
            | Q(full_name__icontains=search)
            | Q(phone__icontains=search)
            | Q(email__icontains=search)
        )

    # Status filter
    if status:
        members = members.filter(status=status)

    paginator = Paginator(members, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        # "members": members,
        "search": search,
        "status": status,
    }

    return render(request, "members/member_list.html", context)


@login_required
def member_create(request):

    if request.method == "POST":

        form = MemberForm(request.POST, request.FILES)

        if form.is_valid():

            form.save()

            return redirect("members:list")

    else:

        form = MemberForm()

    context = {
        "form": form,
    }

    return render(request, "members/member_form.html", context)


@login_required
def member_detail(request, member_id):

    member = Member.objects.get(member_id=member_id)

    return render(
        request,
        "members/member_detail.html",
        {
            "member": member,
        },
    )


@login_required
def member_update(request, member_id):

    member = Member.objects.get(member_id=member_id)

    if request.method == "POST":

        form = MemberForm(request.POST, request.FILES, instance=member)

        if form.is_valid():

            form.save()

            return redirect("members:detail", member_id=member.member_id)

    else:

        form = MemberForm(instance=member)

    return render(
        request,
        "members/member_form.html",
        {
            "form": form,
            "member": member,
        },
    )


@login_required
def member_toggle_status(request, member_id):

    if request.method != "POST":
        return redirect("members:list")

    member = Member.objects.get(member_id=member_id)

    if member.status == "ACTIVE":

        member.status = "INACTIVE"

        messages.success(request, f"{member.full_name} has been deactivated.")

    else:

        member.status = "ACTIVE"

        messages.success(request, f"{member.full_name} has been activated.")

    member.save()

    return redirect("members:list")
