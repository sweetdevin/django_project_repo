from django import forms
from . import models

class menu_item_form(forms.ModelForm):
    class Meta:
        model = models.menu_item
        fields = ['name', 'price', 'blerb']