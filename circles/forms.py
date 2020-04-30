from django import forms
from django.utils import timezone

from .models import Event


class EventHostForm(forms.ModelForm):
    email = forms.EmailField(label="E-Mail-Adresse")

    def clean_start(self):
        start = self.cleaned_data["start"]
        if start < timezone.now():
            raise forms.ValidationError("Muss in der Zukunft sein.")
        return start

    class Meta:
        fields = ["start", "email"]
        model = Event


class JoinForm(forms.Form):
    email = forms.EmailField(label="E-Mail-Adresse")

    class Meta:
        fields = ["email"]
