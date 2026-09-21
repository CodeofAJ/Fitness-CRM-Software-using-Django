from django import forms


from members.models import Member
from .models import MembershipPlan, Membership
from django.utils import timezone




class MembershipPlanForm(forms.ModelForm):

    class Meta:
        model = MembershipPlan

        fields = [
            "name",
            "duration_months",
            "price",
            "description",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "e.g. Monthly",
                }
            ),
            "duration_months": forms.Select(
                attrs={
                    "class": "select select-bordered w-full",
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "e.g. 1500",
                    "step": "0.01",
                    "min": "0",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "placeholder": "Describe what this membership plan includes...",
                    "rows": 4,
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "checkbox checkbox-primary",
                }
            ),
        }



class MembershipForm(forms.ModelForm):

    class Meta:
        model = Membership

        fields = [
            "member",
            "plan",
            "start_date",
            "notes",
        ]

        widgets = {
            "member": forms.Select(
                attrs={
                    "class": "select select-bordered w-full",
                }
            ),

            "plan": forms.Select(
                attrs={
                    "class": "select select-bordered w-full",
                }
            ),

            "start_date": forms.DateInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "type": "date",
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "placeholder": "Add membership notes...",
                    "rows": 4,
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["member"].queryset = (
            Member.objects.filter(
                status="ACTIVE"
            ).order_by("full_name")
        )

        self.fields["plan"].queryset = (
            MembershipPlan.objects.filter(
                is_active=True
            ).order_by(
                "duration_months",
                "price"
            )
        )

        if not self.instance.pk:
            self.fields["start_date"].initial = (
                timezone.localdate()
            )