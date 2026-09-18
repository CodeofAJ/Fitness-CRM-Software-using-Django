from django import forms

from .models import Member


class MemberForm(forms.ModelForm):

    class Meta:
        model = Member

        fields = [
            "member_id",
            "full_name",
            "profile_photo",
            "date_of_birth",
            "gender",
            "phone",
            "email",
            "address",
            "emergency_contact_name",
            "emergency_contact_phone",
            "status",
        ]

        widgets = {
            "member_id": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "e.g. GMS0001",
                }
            ),

            "full_name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Enter full name",
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

            "emergency_contact_name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Emergency contact name",
                }
            ),

            "emergency_contact_phone": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Emergency contact phone",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "select select-bordered w-full",
                }
            ),
        }