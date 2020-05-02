from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from bootstrap_datepicker_plus import DateTimePickerInput

from .models import Event


class Host(forms.ModelForm):
    email = forms.EmailField(label=_("E-mail address"))

    def clean_start(self):
        start = self.cleaned_data["start"]
        if start < timezone.now():
            raise forms.ValidationError(_("Has to be in the future"))
        return start

    class Meta:
        fields = ["start", "email"]
        model = Event

        widgets = {
            'start': DateTimePickerInput(
                options={
                    "format": "MM/DD/YYYY HH:mm", # specify date-frmat
                    "sideBySide": True,
                }
            ),
        }


class Participate(forms.Form):
    email = forms.EmailField(label=_("E-mail address"))

    class Meta:
        fields = ["email"]