from datetime import datetime, timedelta
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from attendance.models import Attendance
from members.models import Member
from memberships.models import Membership, MembershipPlan
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
        "gender_choices": Member.GENDER_CHOICES,
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


@login_required
def membership_report(request):

    today = timezone.localdate()

    memberships = Membership.objects.select_related(
        "member",
        "plan",
    ).all()

    # ---------------------------------------------------------
    # SEARCH
    # ---------------------------------------------------------

    search_query = request.GET.get("q", "").strip()

    if search_query:
        memberships = memberships.filter(
            Q(member__full_name__icontains=search_query)
            | Q(member__member_id__icontains=search_query)
        )

    # ---------------------------------------------------------
    # STATUS FILTER
    # ---------------------------------------------------------

    status_filter = request.GET.get("status", "").strip()

    valid_statuses = [choice[0] for choice in Membership.STATUS_CHOICES]

    if status_filter in valid_statuses:
        memberships = memberships.filter(status=status_filter)

    # ---------------------------------------------------------
    # PLAN FILTER
    # ---------------------------------------------------------

    plan_filter = request.GET.get("plan", "").strip()

    if plan_filter.isdigit():
        memberships = memberships.filter(plan_id=int(plan_filter))

    # ---------------------------------------------------------
    # START DATE FILTER
    # ---------------------------------------------------------

    start_from = request.GET.get("start_from", "").strip()
    start_to = request.GET.get("start_to", "").strip()

    if start_from:
        try:
            parsed_start_from = datetime.strptime(
                start_from,
                "%Y-%m-%d",
            ).date()

            memberships = memberships.filter(start_date__gte=parsed_start_from)

        except ValueError:
            start_from = ""

    if start_to:
        try:
            parsed_start_to = datetime.strptime(
                start_to,
                "%Y-%m-%d",
            ).date()

            memberships = memberships.filter(start_date__lte=parsed_start_to)

        except ValueError:
            start_to = ""

    # ---------------------------------------------------------
    # END DATE FILTER
    # ---------------------------------------------------------

    end_from = request.GET.get("end_from", "").strip()
    end_to = request.GET.get("end_to", "").strip()

    if end_from:
        try:
            parsed_end_from = datetime.strptime(
                end_from,
                "%Y-%m-%d",
            ).date()

            memberships = memberships.filter(end_date__gte=parsed_end_from)

        except ValueError:
            end_from = ""

    if end_to:
        try:
            parsed_end_to = datetime.strptime(
                end_to,
                "%Y-%m-%d",
            ).date()

            memberships = memberships.filter(end_date__lte=parsed_end_to)

        except ValueError:
            end_to = ""

    # ---------------------------------------------------------
    # UPCOMING EXPIRY
    # ---------------------------------------------------------

    expiry_filter = request.GET.get(
        "expiry",
        "",
    ).strip()

    if expiry_filter == "7":
        expiry_date = today + timedelta(days=7)

        memberships = memberships.filter(
            end_date__gte=today,
            end_date__lte=expiry_date,
        )

    elif expiry_filter == "30":
        expiry_date = today + timedelta(days=30)

        memberships = memberships.filter(
            end_date__gte=today,
            end_date__lte=expiry_date,
        )

    # ---------------------------------------------------------
    # REPORT STATISTICS
    # ---------------------------------------------------------

    total_memberships = memberships.count()

    active_memberships = memberships.filter(status="ACTIVE").count()

    expired_memberships = memberships.filter(status="EXPIRED").count()

    pending_memberships = memberships.filter(status="PENDING").count()

    cancelled_memberships = memberships.filter(status="CANCELLED").count()

    # ---------------------------------------------------------
    # PAGINATION
    # ---------------------------------------------------------

    memberships = memberships.order_by(
        "-start_date",
        "-created_at",
    )

    paginator = Paginator(
        memberships,
        10,
    )

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {
        "memberships": page_obj,
        "page_obj": page_obj,
        "total_memberships": total_memberships,
        "active_memberships": active_memberships,
        "expired_memberships": expired_memberships,
        "pending_memberships": pending_memberships,
        "cancelled_memberships": cancelled_memberships,
        "status_choices": Membership.STATUS_CHOICES,
        "plans": MembershipPlan.objects.filter(is_active=True).order_by("name"),
        "search_query": search_query,
        "status_filter": status_filter,
        "plan_filter": plan_filter,
        "start_from": start_from,
        "start_to": start_to,
        "end_from": end_from,
        "end_to": end_to,
        "expiry_filter": expiry_filter,
    }

    return render(
        request,
        "reports/membership_report.html",
        context,
    )


@login_required
def attendance_report(request):

    today = timezone.localdate()

    attendance_records = Attendance.objects.select_related(
        "member",
    ).all()

    # ---------------------------------------------------------
    # SEARCH
    # ---------------------------------------------------------

    search_query = request.GET.get("q", "").strip()

    if search_query:
        attendance_records = attendance_records.filter(
            Q(member__full_name__icontains=search_query)
            | Q(member__member_id__icontains=search_query)
        )

    # ---------------------------------------------------------
    # STATUS FILTER
    # ---------------------------------------------------------

    status_filter = request.GET.get("status", "").strip()

    valid_statuses = [choice[0] for choice in Attendance.STATUS_CHOICES]

    if status_filter in valid_statuses:
        attendance_records = attendance_records.filter(status=status_filter)

    # ---------------------------------------------------------
    # DATE RANGE FILTER
    # ---------------------------------------------------------

    date_from = request.GET.get("date_from", "").strip()
    date_to = request.GET.get("date_to", "").strip()

    if date_from:
        try:
            parsed_date_from = datetime.strptime(
                date_from,
                "%Y-%m-%d",
            ).date()

            attendance_records = attendance_records.filter(date__gte=parsed_date_from)

        except ValueError:
            date_from = ""

    if date_to:
        try:
            parsed_date_to = datetime.strptime(
                date_to,
                "%Y-%m-%d",
            ).date()

            attendance_records = attendance_records.filter(date__lte=parsed_date_to)

        except ValueError:
            date_to = ""

    # ---------------------------------------------------------
    # QUICK DATE FILTER
    # ---------------------------------------------------------

    period_filter = request.GET.get(
        "period",
        "",
    ).strip()

    if period_filter == "today":

        attendance_records = attendance_records.filter(date=today)

    elif period_filter == "7":

        period_start = today - timedelta(days=6)

        attendance_records = attendance_records.filter(
            date__gte=period_start,
            date__lte=today,
        )

    elif period_filter == "30":

        period_start = today - timedelta(days=29)

        attendance_records = attendance_records.filter(
            date__gte=period_start,
            date__lte=today,
        )

    # ---------------------------------------------------------
    # REPORT STATISTICS
    # ---------------------------------------------------------

    total_attendance = attendance_records.count()

    present_attendance = attendance_records.filter(status="PRESENT").count()

    absent_attendance = attendance_records.filter(status="ABSENT").count()

    if total_attendance > 0:
        attendance_rate = round(
            (present_attendance / total_attendance) * 100,
            1,
        )
    else:
        attendance_rate = 0

    # ---------------------------------------------------------
    # PAGINATION
    # ---------------------------------------------------------

    attendance_records = attendance_records.order_by(
        "-date",
        "-check_in",
    )

    paginator = Paginator(
        attendance_records,
        10,
    )

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {
        "attendance_records": page_obj,
        "page_obj": page_obj,
        "total_attendance": total_attendance,
        "present_attendance": present_attendance,
        "absent_attendance": absent_attendance,
        "attendance_rate": attendance_rate,
        "status_choices": Attendance.STATUS_CHOICES,
        "search_query": search_query,
        "status_filter": status_filter,
        "date_from": date_from,
        "date_to": date_to,
        "period_filter": period_filter,
    }

    return render(
        request,
        "reports/attendance_report.html",
        context,
    )


@login_required
def trainer_report(request):

    trainers = Trainer.objects.all()

    # ---------------------------------------------------------
    # SEARCH
    # ---------------------------------------------------------

    search_query = request.GET.get("q", "").strip()

    if search_query:
        trainers = trainers.filter(
            Q(full_name__icontains=search_query)
            | Q(trainer_id__icontains=search_query)
            | Q(phone__icontains=search_query)
            | Q(email__icontains=search_query)
            | Q(specialization__icontains=search_query)
        )

    # ---------------------------------------------------------
    # STATUS FILTER
    # ---------------------------------------------------------

    status_filter = request.GET.get(
        "status",
        "",
    ).strip()

    valid_statuses = [choice[0] for choice in Trainer.STATUS_CHOICES]

    if status_filter in valid_statuses:
        trainers = trainers.filter(status=status_filter)

    # ---------------------------------------------------------
    # GENDER FILTER
    # ---------------------------------------------------------

    gender_filter = request.GET.get(
        "gender",
        "",
    ).strip()

    valid_genders = [choice[0] for choice in Trainer.GENDER_CHOICES]

    if gender_filter in valid_genders:
        trainers = trainers.filter(gender=gender_filter)

    # ---------------------------------------------------------
    # SPECIALIZATION FILTER
    # ---------------------------------------------------------

    specialization_filter = request.GET.get(
        "specialization",
        "",
    ).strip()

    if specialization_filter:
        trainers = trainers.filter(specialization__icontains=specialization_filter)

    # ---------------------------------------------------------
    # JOINING DATE FILTER
    # ---------------------------------------------------------

    joining_from = request.GET.get(
        "joining_from",
        "",
    ).strip()

    joining_to = request.GET.get(
        "joining_to",
        "",
    ).strip()

    if joining_from:
        try:
            parsed_joining_from = datetime.strptime(
                joining_from,
                "%Y-%m-%d",
            ).date()

            trainers = trainers.filter(joining_date__gte=parsed_joining_from)

        except ValueError:
            joining_from = ""

    if joining_to:
        try:
            parsed_joining_to = datetime.strptime(
                joining_to,
                "%Y-%m-%d",
            ).date()

            trainers = trainers.filter(joining_date__lte=parsed_joining_to)

        except ValueError:
            joining_to = ""

    # ---------------------------------------------------------
    # EXPERIENCE FILTER
    # ---------------------------------------------------------

    experience_filter = request.GET.get(
        "experience",
        "",
    ).strip()

    if experience_filter == "0-2":
        trainers = trainers.filter(
            experience_years__gte=0,
            experience_years__lte=2,
        )

    elif experience_filter == "3-5":
        trainers = trainers.filter(
            experience_years__gte=3,
            experience_years__lte=5,
        )

    elif experience_filter == "6-10":
        trainers = trainers.filter(
            experience_years__gte=6,
            experience_years__lte=10,
        )

    elif experience_filter == "10+":
        trainers = trainers.filter(experience_years__gte=11)

    # ---------------------------------------------------------
    # REPORT STATISTICS
    # ---------------------------------------------------------

    total_trainers = trainers.count()

    active_trainers = trainers.filter(status="ACTIVE").count()

    inactive_trainers = trainers.filter(status="INACTIVE").count()

    male_trainers = trainers.filter(gender="MALE").count()

    female_trainers = trainers.filter(gender="FEMALE").count()

    other_trainers = trainers.filter(gender="OTHER").count()

    # ---------------------------------------------------------
    # PAGINATION
    # ---------------------------------------------------------

    trainers = trainers.order_by(
        "-joining_date",
        "-created_at",
    )

    paginator = Paginator(
        trainers,
        10,
    )

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {
        "trainers": page_obj,
        "page_obj": page_obj,
        "total_trainers": total_trainers,
        "active_trainers": active_trainers,
        "inactive_trainers": inactive_trainers,
        "male_trainers": male_trainers,
        "female_trainers": female_trainers,
        "other_trainers": other_trainers,
        "status_choices": Trainer.STATUS_CHOICES,
        "gender_choices": Trainer.GENDER_CHOICES,
        "search_query": search_query,
        "status_filter": status_filter,
        "gender_filter": gender_filter,
        "specialization_filter": specialization_filter,
        "joining_from": joining_from,
        "joining_to": joining_to,
        "experience_filter": experience_filter,
    }

    return render(
        request,
        "reports/trainer_report.html",
        context,
    )


@login_required
def combined_report(request):

    today = timezone.localdate()

    # ---------------------------------------------------------
    # DATE RANGE
    # ---------------------------------------------------------

    date_from = request.GET.get(
        "date_from",
        "",
    ).strip()

    date_to = request.GET.get(
        "date_to",
        "",
    ).strip()

    parsed_date_from = None
    parsed_date_to = None

    if date_from:
        try:
            parsed_date_from = datetime.strptime(
                date_from,
                "%Y-%m-%d",
            ).date()

        except ValueError:
            date_from = ""

    if date_to:
        try:
            parsed_date_to = datetime.strptime(
                date_to,
                "%Y-%m-%d",
            ).date()

        except ValueError:
            date_to = ""

    # ---------------------------------------------------------
    # DEFAULT DATE RANGE
    # ---------------------------------------------------------

    if not parsed_date_from:
        parsed_date_from = today - timedelta(days=29)

    if not parsed_date_to:
        parsed_date_to = today

    # ---------------------------------------------------------
    # MEMBER SUMMARY
    # ---------------------------------------------------------

    total_members = Member.objects.count()

    active_members = Member.objects.filter(status="ACTIVE").count()

    inactive_members = Member.objects.filter(status="INACTIVE").count()

    new_members = Member.objects.filter(
        join_date__gte=parsed_date_from,
        join_date__lte=parsed_date_to,
    ).count()

    # ---------------------------------------------------------
    # MEMBERSHIP SUMMARY
    # ---------------------------------------------------------

    total_memberships = Membership.objects.count()

    active_memberships = Membership.objects.filter(status="ACTIVE").count()

    expired_memberships = Membership.objects.filter(status="EXPIRED").count()

    new_memberships = Membership.objects.filter(
        start_date__gte=parsed_date_from,
        start_date__lte=parsed_date_to,
    ).count()

    # ---------------------------------------------------------
    # ATTENDANCE SUMMARY
    # ---------------------------------------------------------

    attendance_records = Attendance.objects.filter(
        date__gte=parsed_date_from,
        date__lte=parsed_date_to,
    )

    total_attendance = attendance_records.count()

    present_attendance = attendance_records.filter(status="PRESENT").count()

    absent_attendance = attendance_records.filter(status="ABSENT").count()

    if total_attendance > 0:

        attendance_rate = round(
            (present_attendance / total_attendance) * 100,
            1,
        )

    else:

        attendance_rate = 0

    # ---------------------------------------------------------
    # TRAINER SUMMARY
    # ---------------------------------------------------------

    total_trainers = Trainer.objects.count()

    active_trainers = Trainer.objects.filter(status="ACTIVE").count()

    inactive_trainers = Trainer.objects.filter(status="INACTIVE").count()

    new_trainers = Trainer.objects.filter(
        joining_date__gte=parsed_date_from,
        joining_date__lte=parsed_date_to,
    ).count()

    # ---------------------------------------------------------
    # ATTENDANCE BY DAY
    # ---------------------------------------------------------

    attendance_labels = []
    attendance_data = []

    for days_ago in range(6, -1, -1):

        current_date = today - timedelta(days=days_ago)

        present_count = Attendance.objects.filter(
            date=current_date,
            status="PRESENT",
        ).count()

        attendance_labels.append(current_date.strftime("%a"))

        attendance_data.append(present_count)

    # ---------------------------------------------------------
    # RECENT MEMBERS
    # ---------------------------------------------------------

    recent_members = Member.objects.order_by("-created_at")[:5]

    # ---------------------------------------------------------
    # EXPIRING MEMBERSHIPS
    # ---------------------------------------------------------

    upcoming_expiry_date = today + timedelta(days=7)

    expiring_memberships = (
        Membership.objects.filter(
            end_date__gte=today,
            end_date__lte=upcoming_expiry_date,
            status="ACTIVE",
        )
        .select_related(
            "member",
            "plan",
        )
        .order_by("end_date")[:5]
    )

    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------

    context = {
        # Date filters
        "date_from": date_from,
        "date_to": date_to,
        # Members
        "total_members": total_members,
        "active_members": active_members,
        "inactive_members": inactive_members,
        "new_members": new_members,
        # Memberships
        "total_memberships": total_memberships,
        "active_memberships": active_memberships,
        "expired_memberships": expired_memberships,
        "new_memberships": new_memberships,
        # Attendance
        "total_attendance": total_attendance,
        "present_attendance": present_attendance,
        "absent_attendance": absent_attendance,
        "attendance_rate": attendance_rate,
        # Trainers
        "total_trainers": total_trainers,
        "active_trainers": active_trainers,
        "inactive_trainers": inactive_trainers,
        "new_trainers": new_trainers,
        # Dashboard information
        "attendance_labels": attendance_labels,
        "attendance_data": attendance_data,
        "recent_members": recent_members,
        "expiring_memberships": expiring_memberships,
    }

    return render(
        request,
        "reports/combined_report.html",
        context,
    )


def pdf_styles():
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontSize=20,
        leading=24,
        alignment=TA_CENTER,
        spaceAfter=8,
    )

    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        textColor=colors.grey,
        spaceAfter=15,
    )

    heading_style = ParagraphStyle(
        "ReportHeading",
        parent=styles["Heading2"],
        fontSize=13,
        leading=16,
        spaceBefore=8,
        spaceAfter=8,
    )

    normal_style = ParagraphStyle(
        "ReportNormal",
        parent=styles["Normal"],
        fontSize=8,
        leading=11,
    )

    return {
        "title": title_style,
        "subtitle": subtitle_style,
        "heading": heading_style,
        "normal": normal_style,
    }


def create_pdf_response(filename):

    buffer = BytesIO()

    response = HttpResponse(content_type="application/pdf")

    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    return buffer, response


def build_report_header(
    story,
    title,
    subtitle,
    styles,
):

    story.append(
        Paragraph(
            "GMS — Gym Management System",
            styles["title"],
        )
    )

    story.append(
        Paragraph(
            title,
            styles["heading"],
        )
    )

    story.append(
        Paragraph(
            subtitle,
            styles["subtitle"],
        )
    )

    story.append(
        Spacer(
            1,
            5 * mm,
        )
    )


@login_required
def member_report_pdf(request):

    members = Member.objects.all()

    search_query = request.GET.get(
        "q",
        "",
    ).strip()

    if search_query:
        members = members.filter(
            Q(full_name__icontains=search_query)
            | Q(member_id__icontains=search_query)
            | Q(phone__icontains=search_query)
            | Q(email__icontains=search_query)
        )

    status_filter = request.GET.get(
        "status",
        "",
    ).strip()

    if status_filter in [choice[0] for choice in Member.STATUS_CHOICES]:
        members = members.filter(status=status_filter)

    gender_filter = request.GET.get(
        "gender",
        "",
    ).strip()

    if gender_filter in [choice[0] for choice in Member.GENDER_CHOICES]:
        members = members.filter(gender=gender_filter)

    date_from = request.GET.get(
        "date_from",
        "",
    ).strip()

    date_to = request.GET.get(
        "date_to",
        "",
    ).strip()

    if date_from:
        try:
            parsed_date = datetime.strptime(
                date_from,
                "%Y-%m-%d",
            ).date()

            members = members.filter(join_date__gte=parsed_date)

        except ValueError:
            pass

    if date_to:
        try:
            parsed_date = datetime.strptime(
                date_to,
                "%Y-%m-%d",
            ).date()

            members = members.filter(join_date__lte=parsed_date)

        except ValueError:
            pass

    members = members.order_by("-join_date")

    styles = pdf_styles()

    buffer, response = create_pdf_response("member-report.pdf")

    document = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=10 * mm,
        leftMargin=10 * mm,
        topMargin=10 * mm,
        bottomMargin=10 * mm,
    )

    story = []

    build_report_header(
        story,
        "Member Report",
        f"Generated on {timezone.localdate().strftime('%d %B %Y')}",
        styles,
    )

    data = [
        [
            "Member ID",
            "Name",
            "Gender",
            "Phone",
            "Email",
            "Join Date",
            "Status",
        ]
    ]

    for member in members:

        data.append(
            [
                member.member_id,
                member.full_name,
                member.get_gender_display(),
                member.phone,
                member.email or "-",
                member.join_date.strftime("%d %b %Y"),
                member.get_status_display(),
            ]
        )

    table = Table(
        data,
        repeatRows=1,
        colWidths=[
            25 * mm,
            40 * mm,
            25 * mm,
            30 * mm,
            55 * mm,
            30 * mm,
            25 * mm,
        ],
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#ff4000"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#fff3ee"),
                    ],
                ),
            ]
        )
    )

    story.append(table)

    document.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    response.write(pdf)

    return response


@login_required
def membership_report_pdf(request):

    memberships = Membership.objects.select_related(
        "member",
        "plan",
    ).all()

    search_query = request.GET.get(
        "q",
        "",
    ).strip()

    if search_query:
        memberships = memberships.filter(
            Q(member__full_name__icontains=search_query)
            | Q(member__member_id__icontains=search_query)
        )

    status_filter = request.GET.get(
        "status",
        "",
    ).strip()

    if status_filter in [choice[0] for choice in Membership.STATUS_CHOICES]:
        memberships = memberships.filter(status=status_filter)

    plan_filter = request.GET.get(
        "plan",
        "",
    ).strip()

    if plan_filter.isdigit():
        memberships = memberships.filter(plan_id=int(plan_filter))

    memberships = memberships.order_by(
        "-start_date",
        "-created_at",
    )

    styles = pdf_styles()

    buffer, response = create_pdf_response("membership-report.pdf")

    document = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=10 * mm,
        leftMargin=10 * mm,
        topMargin=10 * mm,
        bottomMargin=10 * mm,
    )

    story = []

    build_report_header(
        story,
        "Membership Report",
        f"Generated on {timezone.localdate().strftime('%d %B %Y')}",
        styles,
    )

    data = [
        [
            "Member",
            "Member ID",
            "Plan",
            "Start Date",
            "End Date",
            "Status",
        ]
    ]

    for membership in memberships:

        data.append(
            [
                membership.member.full_name,
                membership.member.member_id,
                str(membership.plan),
                membership.start_date.strftime("%d %b %Y"),
                membership.end_date.strftime("%d %b %Y"),
                membership.get_status_display(),
            ]
        )

    table = Table(
        data,
        repeatRows=1,
        colWidths=[
            45 * mm,
            30 * mm,
            40 * mm,
            30 * mm,
            30 * mm,
            30 * mm,
        ],
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#ff4000"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#fff3ee"),
                    ],
                ),
            ]
        )
    )

    story.append(table)

    document.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    response.write(pdf)

    return response


@login_required
def attendance_report_pdf(request):

    attendance_records = Attendance.objects.select_related(
        "member",
    ).all()

    search_query = request.GET.get(
        "q",
        "",
    ).strip()

    if search_query:
        attendance_records = attendance_records.filter(
            Q(member__full_name__icontains=search_query)
            | Q(member__member_id__icontains=search_query)
        )

    status_filter = request.GET.get(
        "status",
        "",
    ).strip()

    if status_filter in [choice[0] for choice in Attendance.STATUS_CHOICES]:
        attendance_records = attendance_records.filter(status=status_filter)

    date_from = request.GET.get(
        "date_from",
        "",
    ).strip()

    date_to = request.GET.get(
        "date_to",
        "",
    ).strip()

    if date_from:
        try:
            parsed_date = datetime.strptime(
                date_from,
                "%Y-%m-%d",
            ).date()

            attendance_records = attendance_records.filter(date__gte=parsed_date)

        except ValueError:
            pass

    if date_to:
        try:
            parsed_date = datetime.strptime(
                date_to,
                "%Y-%m-%d",
            ).date()

            attendance_records = attendance_records.filter(date__lte=parsed_date)

        except ValueError:
            pass

    attendance_records = attendance_records.order_by(
        "-date",
        "-check_in",
    )

    styles = pdf_styles()

    buffer, response = create_pdf_response("attendance-report.pdf")

    document = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=10 * mm,
        leftMargin=10 * mm,
        topMargin=10 * mm,
        bottomMargin=10 * mm,
    )

    story = []

    build_report_header(
        story,
        "Attendance Report",
        f"Generated on {timezone.localdate().strftime('%d %B %Y')}",
        styles,
    )

    data = [
        [
            "Member",
            "Member ID",
            "Date",
            "Check In",
            "Check Out",
            "Status",
        ]
    ]

    for attendance in attendance_records:

        data.append(
            [
                attendance.member.full_name,
                attendance.member.member_id,
                attendance.date.strftime("%d %b %Y"),
                (
                    attendance.check_in.strftime("%I:%M %p")
                    if attendance.check_in
                    else "-"
                ),
                (
                    attendance.check_out.strftime("%I:%M %p")
                    if attendance.check_out
                    else "-"
                ),
                attendance.get_status_display(),
            ]
        )

    table = Table(
        data,
        repeatRows=1,
        colWidths=[
            50 * mm,
            30 * mm,
            30 * mm,
            30 * mm,
            30 * mm,
            30 * mm,
        ],
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#ff4000"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#fff3ee"),
                    ],
                ),
            ]
        )
    )

    story.append(table)

    document.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    response.write(pdf)

    return response


@login_required
def trainer_report_pdf(request):

    trainers = Trainer.objects.all()

    search_query = request.GET.get(
        "q",
        "",
    ).strip()

    if search_query:
        trainers = trainers.filter(
            Q(full_name__icontains=search_query)
            | Q(trainer_id__icontains=search_query)
            | Q(phone__icontains=search_query)
            | Q(email__icontains=search_query)
            | Q(specialization__icontains=search_query)
        )

    status_filter = request.GET.get(
        "status",
        "",
    ).strip()

    if status_filter in [choice[0] for choice in Trainer.STATUS_CHOICES]:
        trainers = trainers.filter(status=status_filter)

    gender_filter = request.GET.get(
        "gender",
        "",
    ).strip()

    if gender_filter in [choice[0] for choice in Trainer.GENDER_CHOICES]:
        trainers = trainers.filter(gender=gender_filter)

    trainers = trainers.order_by("-joining_date")

    styles = pdf_styles()

    buffer, response = create_pdf_response("trainer-report.pdf")

    document = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=10 * mm,
        leftMargin=10 * mm,
        topMargin=10 * mm,
        bottomMargin=10 * mm,
    )

    story = []

    build_report_header(
        story,
        "Trainer Report",
        f"Generated on {timezone.localdate().strftime('%d %B %Y')}",
        styles,
    )

    data = [
        [
            "Trainer ID",
            "Name",
            "Specialization",
            "Experience",
            "Joining Date",
            "Gender",
            "Status",
        ]
    ]

    for trainer in trainers:

        data.append(
            [
                trainer.trainer_id,
                trainer.full_name,
                trainer.specialization,
                f"{trainer.experience_years} years",
                trainer.joining_date.strftime("%d %b %Y"),
                trainer.get_gender_display(),
                trainer.get_status_display(),
            ]
        )

    table = Table(
        data,
        repeatRows=1,
        colWidths=[
            25 * mm,
            40 * mm,
            45 * mm,
            30 * mm,
            30 * mm,
            25 * mm,
            25 * mm,
        ],
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#ff4000"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#fff3ee"),
                    ],
                ),
            ]
        )
    )

    story.append(table)

    document.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    response.write(pdf)

    return response


@login_required
def combined_report_pdf(request):

    today = timezone.localdate()

    date_from = request.GET.get(
        "date_from",
        "",
    ).strip()

    date_to = request.GET.get(
        "date_to",
        "",
    ).strip()

    parsed_date_from = None
    parsed_date_to = None

    if date_from:
        try:
            parsed_date_from = datetime.strptime(
                date_from,
                "%Y-%m-%d",
            ).date()
        except ValueError:
            date_from = ""

    if date_to:
        try:
            parsed_date_to = datetime.strptime(
                date_to,
                "%Y-%m-%d",
            ).date()
        except ValueError:
            date_to = ""

    if not parsed_date_from:
        parsed_date_from = today - timedelta(days=29)

    if not parsed_date_to:
        parsed_date_to = today

    total_members = Member.objects.count()

    active_members = Member.objects.filter(status="ACTIVE").count()

    inactive_members = Member.objects.filter(status="INACTIVE").count()

    new_members = Member.objects.filter(
        join_date__gte=parsed_date_from,
        join_date__lte=parsed_date_to,
    ).count()

    total_memberships = Membership.objects.count()

    active_memberships = Membership.objects.filter(status="ACTIVE").count()

    expired_memberships = Membership.objects.filter(status="EXPIRED").count()

    new_memberships = Membership.objects.filter(
        start_date__gte=parsed_date_from,
        start_date__lte=parsed_date_to,
    ).count()

    attendance_records = Attendance.objects.filter(
        date__gte=parsed_date_from,
        date__lte=parsed_date_to,
    )

    total_attendance = attendance_records.count()

    present_attendance = attendance_records.filter(status="PRESENT").count()

    absent_attendance = attendance_records.filter(status="ABSENT").count()

    if total_attendance:

        attendance_rate = round(
            present_attendance / total_attendance * 100,
            1,
        )

    else:

        attendance_rate = 0

    total_trainers = Trainer.objects.count()

    active_trainers = Trainer.objects.filter(status="ACTIVE").count()

    inactive_trainers = Trainer.objects.filter(status="INACTIVE").count()

    new_trainers = Trainer.objects.filter(
        joining_date__gte=parsed_date_from,
        joining_date__lte=parsed_date_to,
    ).count()

    styles = pdf_styles()

    buffer, response = create_pdf_response("combined-report.pdf")

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )

    story = []

    build_report_header(
        story,
        "Combined Management Report",
        (
            f"Period: "
            f"{parsed_date_from.strftime('%d %b %Y')} "
            f"to "
            f"{parsed_date_to.strftime('%d %b %Y')}"
        ),
        styles,
    )

    # ---------------------------------------------------------
    # MEMBERS
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Members",
            styles["heading"],
        )
    )

    member_data = [
        ["Metric", "Count"],
        ["Total Members", total_members],
        ["Active Members", active_members],
        ["Inactive Members", inactive_members],
        ["New Members in Period", new_members],
    ]

    member_table = Table(
        member_data,
        colWidths=[
            100 * mm,
            50 * mm,
        ],
    )

    member_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#ff4000"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#fff3ee"),
                    ],
                ),
            ]
        )
    )

    story.append(member_table)

    story.append(
        Spacer(
            1,
            8 * mm,
        )
    )

    # ---------------------------------------------------------
    # MEMBERSHIPS
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Memberships",
            styles["heading"],
        )
    )

    membership_data = [
        ["Metric", "Count"],
        ["Total Memberships", total_memberships],
        ["Active Memberships", active_memberships],
        ["Expired Memberships", expired_memberships],
        ["New Memberships in Period", new_memberships],
    ]

    membership_table = Table(
        membership_data,
        colWidths=[
            100 * mm,
            50 * mm,
        ],
    )

    membership_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#ff4000"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#fff3ee"),
                    ],
                ),
            ]
        )
    )

    story.append(membership_table)

    story.append(
        Spacer(
            1,
            8 * mm,
        )
    )

    # ---------------------------------------------------------
    # ATTENDANCE
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Attendance",
            styles["heading"],
        )
    )

    attendance_data = [
        ["Metric", "Count"],
        ["Total Attendance Records", total_attendance],
        ["Present", present_attendance],
        ["Absent", absent_attendance],
        ["Attendance Rate", f"{attendance_rate}%"],
    ]

    attendance_table = Table(
        attendance_data,
        colWidths=[
            100 * mm,
            50 * mm,
        ],
    )

    attendance_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#ff4000"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#fff3ee"),
                    ],
                ),
            ]
        )
    )

    story.append(attendance_table)

    story.append(
        Spacer(
            1,
            8 * mm,
        )
    )

    # ---------------------------------------------------------
    # TRAINERS
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Trainers",
            styles["heading"],
        )
    )

    trainer_data = [
        ["Metric", "Count"],
        ["Total Trainers", total_trainers],
        ["Active Trainers", active_trainers],
        ["Inactive Trainers", inactive_trainers],
        ["New Trainers in Period", new_trainers],
    ]

    trainer_table = Table(
        trainer_data,
        colWidths=[
            100 * mm,
            50 * mm,
        ],
    )

    trainer_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#ff4000"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#fff3ee"),
                    ],
                ),
            ]
        )
    )

    story.append(trainer_table)

    document.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    response.write(pdf)

    return response
