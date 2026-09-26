from django import forms

from .models import Trainer


class TrainerForm(forms.ModelForm):

    class Meta:
        model = Trainer

        fields = [
            "trainer_id",
            "full_name",
            "profile_photo",
            "date_of_birth",
            "gender",
            "phone",
            "email",
            "address",
            "specialization",
            "experience_years",
            "joining_date",
            "salary",
            "status",
            "bio",
        ]

        widgets = {
            "trainer_id": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "e.g. TR001",
                }
            ),

            "full_name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Enter trainer name",
                }
            ),

            "profile_photo": forms.ClearableFileInput(
                attrs={
                    "class": "file-input file-input-bordered w-full",
                }
            ),

            "date_of_birth": forms.DateInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "type": "date",
                }
            ),

            "gender": forms.Select(
                attrs={
                    "class": "select select-bordered w-full",
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
                    "placeholder": "Enter email address",
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "placeholder": "Enter address",
                    "rows": 3,
                }
            ),

            "specialization": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "e.g. Strength Training",
                }
            ),

            "experience_years": forms.NumberInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "min": "0",
                    "placeholder": "Years of experience",
                }
            ),

            "joining_date": forms.DateInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "type": "date",
                }
            ),

            "salary": forms.NumberInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "Monthly salary",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "select select-bordered w-full",
                }
            ),

            "bio": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "placeholder": "Tell us about the trainer...",
                    "rows": 4,
                }
            ),
        }