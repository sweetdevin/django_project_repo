from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, FormView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login
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

class Menu_detail_view(DetailView):
    model=models.menu_item
    template_name='django_delights/menu_detail.html'
    context_object_name='menu_item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ingredient_list = models.recipe_item.objects.filter(dish=self.object)

        total_cost = sum(ingredient.amount * ingredient.item.cost_per_unit for ingredient in ingredient_list)
        if not total_cost:
            total_cost = 0
        profit_per_dish = context['menu_item'].price - total_cost
        context['ingredients'] = ingredient_list
        context['total_cost'] = total_cost
        context['profit_per_dish'] = profit_per_dish

        import pprint
        pprint.pprint(context)

        return context

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
    
def register(request):
    if request.method == 'POST':
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  # Auto-login after registration
            return redirect('index')  # Redirect to menu list or another page
    else:
        form = forms.UserRegisterForm()
    
    return render(request, 'users/register.html', {'form': form})

class recipe_item_createview(CreateView):
    model =models.recipe_item
    template_name = 'django_delights/recipe_form.html'
    form_class = forms.recipe_form
    
    def form_valid(self, form):
        dish = get_object_or_404(models.menu_item, pk=self.kwargs["pk"])
        form.instance.dish = dish  # Set the recipe before saving
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("menu_detail", kwargs={"pk": self.kwargs["pk"]})