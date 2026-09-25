from django import forms

from .models import Payment


class CashPaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = [
            "member",
            "membership",
            "amount",
            "notes",
        ]

        widgets = {
            "member": forms.Select(
                attrs={
                    "class": "select select-bordered w-full",
                }
            ),
            "membership": forms.Select(
                attrs={
                    "class": "select select-bordered w-full",
                }
            ),
            "amount": forms.NumberInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "e.g. 1500",
                    "step": "0.01",
                    "min": "0",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "placeholder": "Add payment notes...",
                    "rows": 4,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["member"].queryset = (
            self.fields["member"].queryset
            .filter(status="ACTIVE")
            .order_by("full_name")
        )

        self.fields["membership"].queryset = (
            self.fields["membership"].queryset
            .select_related("member", "plan")
            .order_by("-created_at")
        )