from django import forms

from .models import Event


class EventHostForm(forms.ModelForm):
    email = forms.EmailField(label="E-Mail-Adresse")

    class Meta:
        fields = ["start", "email"]
        model = Event
