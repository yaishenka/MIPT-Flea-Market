from django import forms

from .models import AbstractAd

class AbstractAdForm(forms.ModelForm):
    class Meta:
        model = AbstractAd
        fields = ('text', 'category', 'header', 'image')

