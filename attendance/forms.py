from django import forms

from members.models import Member


class AttendanceCheckInForm(forms.Form):

    member = forms.ModelChoiceField(
        queryset=Member.objects.none(),
        widget=forms.Select(
            attrs={
                "class": "select select-bordered w-full",
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["member"].queryset = (
            Member.objects
            .filter(status="ACTIVE")
            .order_by("full_name")
        )