from django import forms

from .models import GymSettings


class GymSettingsForm(forms.ModelForm):

    class Meta:
        model = GymSettings

        fields = [
            "gym_name",
            "phone",
            "email",
            "website",
            "address",
            "description",
        ]

        widgets = {

            "gym_name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Enter gym name",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Enter phone number",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Enter gym email",
                }
            ),

            "website": forms.URLInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "https://example.com",
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "rows": 3,
                    "placeholder": "Enter gym address",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "rows": 4,
                    "placeholder": "Describe your gym",
                }
            ),
        }