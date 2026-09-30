from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import GymSettingsForm
from .models import GymSettings


@login_required
def settings_page(request):

    settings_obj = GymSettings.objects.first()

    if settings_obj is None:
        settings_obj = GymSettings.objects.create(
            gym_name="GMS Gym"
        )

    if request.method == "POST":

        form = GymSettingsForm(
            request.POST,
            instance=settings_obj,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Gym settings updated successfully."
            )

            return redirect("settings_app:settings")

    else:

        form = GymSettingsForm(
            instance=settings_obj
        )

    context = {
        "form": form,
        "settings_obj": settings_obj,
    }

    return render(
        request,
        "settings/settings.html",
        context,
    )