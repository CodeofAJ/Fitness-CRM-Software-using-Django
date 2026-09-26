from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TrainerForm
from .models import Trainer


@login_required
def trainer_list(request):

    search = request.GET.get(
        "search",
        ""
    ).strip()

    status = request.GET.get(
        "status",
        ""
    ).strip()

    trainers = Trainer.objects.all()

    if search:
        trainers = trainers.filter(
            Q(trainer_id__icontains=search)
            | Q(full_name__icontains=search)
            | Q(phone__icontains=search)
            | Q(email__icontains=search)
            | Q(specialization__icontains=search)
        )

    if status:
        trainers = trainers.filter(
            status=status
        )

    paginator = Paginator(
        trainers,
        10
    )

    page_number = request.GET.get(
        "page"
    )

    page_obj = paginator.get_page(
        page_number
    )

    return render(
        request,
        "trainers/trainer_list.html",
        {
            "page_obj": page_obj,
            "trainers": page_obj.object_list,
            "search": search,
            "status": status,
        }
    )


@login_required
def trainer_create(request):

    if request.method == "POST":

        form = TrainerForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            trainer = form.save()

            messages.success(
                request,
                f"{trainer.full_name} was added successfully."
            )

            return redirect(
                "trainers:detail",
                trainer_id=trainer.trainer_id
            )

    else:

        form = TrainerForm()

    return render(
        request,
        "trainers/trainer_form.html",
        {
            "form": form,
            "page_title": "Add Trainer",
            "submit_text": "Add Trainer",
        }
    )


@login_required
def trainer_detail(request, trainer_id):

    trainer = get_object_or_404(
        Trainer,
        trainer_id=trainer_id
    )

    return render(
        request,
        "trainers/trainer_detail.html",
        {
            "trainer": trainer,
        }
    )


@login_required
def trainer_update(request, trainer_id):

    trainer = get_object_or_404(
        Trainer,
        trainer_id=trainer_id
    )

    if request.method == "POST":

        form = TrainerForm(
            request.POST,
            request.FILES,
            instance=trainer
        )

        if form.is_valid():

            trainer = form.save()

            messages.success(
                request,
                f"{trainer.full_name} was updated successfully."
            )

            return redirect(
                "trainers:detail",
                trainer_id=trainer.trainer_id
            )

    else:

        form = TrainerForm(
            instance=trainer
        )

    return render(
        request,
        "trainers/trainer_form.html",
        {
            "form": form,
            "trainer": trainer,
            "page_title": "Edit Trainer",
            "submit_text": "Save Changes",
        }
    )


@login_required
def trainer_toggle_status(request, trainer_id):

    trainer = get_object_or_404(
        Trainer,
        trainer_id=trainer_id
    )

    if trainer.status == "ACTIVE":

        trainer.status = "INACTIVE"

        message = (
            f"{trainer.full_name} has been deactivated."
        )

    else:

        trainer.status = "ACTIVE"

        message = (
            f"{trainer.full_name} has been activated."
        )

    trainer.save(
        update_fields=[
            "status",
            "updated_at",
        ]
    )

    messages.success(
        request,
        message
    )

    return redirect(
        "trainers:detail",
        trainer_id=trainer.trainer_id
    )