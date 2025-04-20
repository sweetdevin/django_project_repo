from django.contrib.auth.models import User
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
    quantity = forms.DecimalField(max_digits=2, initial=0)
    units_of_measure= forms.CharField(required=False, empty_value='???')
    cost_per_unit = forms.DecimalField(max_digits=3, required=False, initial=0.00)

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Passwords do not match.")

        return cleaned_data
class recipe_form(forms.ModelForm):
    class Meta:
        model=models.recipe_item
        fields = ['item', 'amount',]

class purchase_form(forms.ModelForm):
    class Meta:
        model=models.purchases
        fields = ['item', 'quantity']

class review_form(forms.ModelForm):
    class Meta:
        model=models.review
        fields = ['text']