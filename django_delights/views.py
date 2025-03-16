from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, FormView
from django.urls import reverse_lazy
from . import models
from . import forms

# Create your views here.
def index(request):
    return render(request, 'django_delights/index.html')

class menu_view(ListView):
    model=models.menu_item
    template_name='django_delights/menu.html'
    context_object_name='menu_list'

class Menu_item_create_view(CreateView):
    model=models.menu_item
    template_name='django_delights/menu_form.html'
    fields=['name', 'price', 'blerb']
    success_url=reverse_lazy('menu')

class ingredient_view(ListView):
    model=models.Ingredient
    template_name='django_delights/inventory.html'
    context_object_name='ingredient_list'

class InventoryCreateUpdateView(FormView):
    template_name = 'django_delights/inventory_form.html'
    form_class = forms.inventory_form

    def form_valid(self, form):
        name = form.cleaned_data['name']
        quantity = form.cleaned_data['quantity']
        cost_per_unit = form.cleaned_data['cost_per_unit']
        units_of_measure = form.cleaned_data['units_of_measure']

        item, created = models.Ingredient.objects.get_or_create(
            name=name,
            defaults={'cost_per_unit': cost_per_unit, 'quantity': 0,
                      'units_of_measure': units_of_measure}
        )

        if not created:
            item.quantity += quantity
            if cost_per_unit > 0:
                item.cost_per_unit = cost_per_unit
            if units_of_measure != "???":
                item.units_of_measure = units_of_measure
        else:
            item.quantity = quantity

        item.save()
        return redirect('inventory')