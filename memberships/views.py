from datetime import date
from calendar import monthrange


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MembershipForm, MembershipPlanForm
from .models import Membership, MembershipPlan


@login_required
def plan_list(request):

    search = request.GET.get("search", "").strip()
    status = request.GET.get("status", "").strip()

    plans = MembershipPlan.objects.all()

    if search:
        plans = plans.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )

    if status == "ACTIVE":
        plans = plans.filter(is_active=True)

    elif status == "INACTIVE":
        plans = plans.filter(is_active=False)

    context = {
        "plans": plans,
        "search": search,
        "status": status,
    }

    return render(request, "memberships/plan_list.html", context)


@login_required
def plan_create(request):

    if request.method == "POST":

        form = MembershipPlanForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Membership plan created successfully.")

            return redirect("memberships:plan_list")

    else:

        form = MembershipPlanForm()

    return render(
        request,
        "memberships/plan_form.html",
        {
            "form": form,
        },
    )


@login_required
def plan_update(request, pk):

    plan = get_object_or_404(MembershipPlan, pk=pk)

    if request.method == "POST":

        form = MembershipPlanForm(request.POST, instance=plan)

        if form.is_valid():

            form.save()

            messages.success(request, "Membership plan updated successfully.")

            return redirect("memberships:plan_list")

    else:

        form = MembershipPlanForm(instance=plan)

    return render(
        request,
        "memberships/plan_form.html",
        {
            "form": form,
            "plan": plan,
        },
    )


@login_required
def plan_toggle_status(request, pk):

    if request.method != "POST":
        return redirect("memberships:plan_list")

    plan = get_object_or_404(MembershipPlan, pk=pk)

    plan.is_active = not plan.is_active

    plan.save()

    if plan.is_active:

        messages.success(request, f"{plan.name} has been activated.")

    else:

        messages.success(request, f"{plan.name} has been deactivated.")

    return redirect("memberships:plan_list")


@login_required
def membership_list(request):

    search = request.GET.get("search", "").strip()
    status = request.GET.get("status", "").strip()

    memberships = Membership.objects.select_related("member", "plan").all()

    if search:
        memberships = memberships.filter(
            Q(member__member_id__icontains=search)
            | Q(member__full_name__icontains=search)
            | Q(member__phone__icontains=search)
            | Q(plan__name__icontains=search)
        )

    if status:
        memberships = memberships.filter(status=status)

    context = {
        "memberships": memberships,
        "search": search,
        "status": status,
    }

    return render(request, "memberships/membership_list.html", context)


def calculate_end_date(start_date, duration_months):

    month = start_date.month - 1 + duration_months

    year = start_date.year + month // 12

    month = month % 12 + 1

    day = min(start_date.day, monthrange(year, month)[1])

    return date(year, month, day)


@login_required
def membership_create(request):

    if request.method == "POST":

        form = MembershipForm(request.POST)

        if form.is_valid():

            membership = form.save(commit=False)

            membership.status = "ACTIVE"

            membership.end_date = calculate_end_date(
                membership.start_date, membership.plan.duration_months
            )

            from datetime import timedelta

            membership.end_date -= timedelta(days=1)

            membership.save()

            messages.success(request, "Membership assigned successfully.")

            return redirect("memberships:membership_detail", pk=membership.pk)

    else:

        form = MembershipForm()

    return render(
        request,
        "memberships/membership_form.html",
        {
            "form": form,
        },
    )


@login_required
def membership_detail(request, pk):

    membership = get_object_or_404(
        Membership.objects.select_related("member", "plan"), pk=pk
    )

    return render(
        request,
        "memberships/membership_detail.html",
        {
            "membership": membership,
        },
    )
