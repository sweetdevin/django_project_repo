from django import forms
from . import models

class menu_item_form(forms.ModelForm):
    class Meta:
        model = models.menu_item
        fields = ['name', 'price', 'blerb']

class inventory_form(forms.ModelForm):
    class Meta:
        model = models.Ingredient
        fields = ['name', 'quantity', 'units_of_measure', 'cost_per_unit']