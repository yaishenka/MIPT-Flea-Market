"""FleaMarket app forms"""
from django import forms
from .models import AbstractAd

class AbstractAdForm(forms.ModelForm):
    """Form to add/edit AbstractAdd model"""
    class Meta:
        """AbstractAd meta class"""
        model = AbstractAd
        fields = ('text', 'category', 'header', 'image')
