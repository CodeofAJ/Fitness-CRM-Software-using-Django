from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render
from trainers.models import Trainer

from .forms import MemberForm
from .models import Member



@login_required
def dashboard(request):

    total_trainers = Trainer.objects.count()

    active_trainers = Trainer.objects.filter(
        status="ACTIVE"
    ).count()

    inactive_trainers = Trainer.objects.filter(
        status="INACTIVE"
    ).count()

    context = {
        "total_trainers": total_trainers,
        "active_trainers": active_trainers,
        "inactive_trainers": inactive_trainers,
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

    return render(
        request,
        "members/member_list.html",
        context
    )



@login_required
def member_create(request):

    if request.method == "POST":

        form = MemberForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect("members:list")

    else:

        form = MemberForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "members/member_form.html",
        context
    )



@login_required
def member_detail(request, member_id):

    member = Member.objects.get(
        member_id=member_id
    )

    return render(
        request,
        "members/member_detail.html",
        {
            "member": member,
        }
    )


@login_required
def member_update(request, member_id):

    member = Member.objects.get(
        member_id=member_id
    )

    if request.method == "POST":

        form = MemberForm(
            request.POST,
            request.FILES,
            instance=member
        )

        if form.is_valid():

            form.save()

            return redirect(
                "members:detail",
                member_id=member.member_id
            )

    else:

        form = MemberForm(
            instance=member
        )

    return render(
        request,
        "members/member_form.html",
        {
            "form": form,
            "member": member,
        }
    )


@login_required
def member_toggle_status(request, member_id):

    if request.method != "POST":
        return redirect("members:list")

    member = Member.objects.get(
        member_id=member_id
    )

    if member.status == "ACTIVE":

        member.status = "INACTIVE"

        messages.success(
            request,
            f"{member.full_name} has been deactivated."
        )

    else:

        member.status = "ACTIVE"

        messages.success(
            request,
            f"{member.full_name} has been activated."
        )

    member.save()

    return redirect("members:list")