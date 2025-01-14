from django import forms

from .models import Civi


class CiviForm(forms.ModelForm):
    """Form for creating civis"""

    class Meta:
        model = Civi
        fields = ["author", "thread", "title", "body", "c_type"]
        widgets = {
            "body": forms.Textarea(
                attrs={"class": "materialize-textarea", "length": "1000"}
            ),
            "c_type": forms.HiddenInput(),
        }
