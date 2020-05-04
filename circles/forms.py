from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from bootstrap_datepicker_plus import DateTimePickerInput
from django.utils.translation import get_language
from django.utils import formats

from .models import Event


class Host(forms.ModelForm):
    email = forms.EmailField(label=_("E-mail address"))

    def clean_start(self):
        start = self.cleaned_data["start"]
        if start < timezone.now():
            raise forms.ValidationError(_("Has to be in the future"))
        return start

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        locale_formats = formats.get_format("DATETIME_INPUT_FORMATS")
        self.fields["start"].widget = DateTimePickerInput(
            format=locale_formats[2],  # format without seconds
            options={"sideBySide": True, "locale": get_language()},
        )

    class Meta:
        fields = ["start", "email"]
        model = Event


class Participate(forms.Form):
    email = forms.EmailField(label=_("E-mail address"))

    class Meta:
        fields = ["email"]
