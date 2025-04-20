from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, FormView, FormMixin, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from . import models
from . import forms
from math import floor

# Create your views here.
def index(request):
    return render(request, 'django_delights/index.html')

class menu_view(FormMixin, ListView):
    model=models.menu_item
    template_name='django_delights/menu.html'
    context_object_name='menu_list'
    form_class = forms.purchase_form
    success_url = reverse_lazy('menu')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        available_context = []
        for menu_item in context['menu_list']:
            available = True
            min_available = None
            recipe_list = models.recipe_item.objects.filter(dish=menu_item)
            for recipe_item in recipe_list:
                ingredient = recipe_item.item
                if recipe_item.amount <= ingredient.quantity:
                    num_available = ingredient.quantity/recipe_item.amount
                    if min_available == None:
                        min_available = num_available
                    elif num_available < min_available:
                        min_available = num_available
                else:
                    available = False
            if available == True:
                available_context.append({'menu_item':menu_item, 'quantity_available': floor(min_available)})
        context['available_list'] = available_context
        return context                


    def post(self, request, *args, **kwargs):
        form = self.get_form()  
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form) 
        
    def form_valid(self, form): 
        purchase = form.save(commit=False)
        menu_object = purchase.item
        ingredient_list = models.recipe_item.objects.filter(dish=menu_object)
        for ingredient in ingredient_list:
            pantry_item = ingredient.item
            total_used = ingredient.amount * purchase.quantity
            pantry_item.quantity -= total_used
            pantry_item.save()
        purchase.save()
        messages.success(self.request, f"✅ {form.cleaned_data['quantity']}x {form.cleaned_data['item']} purchased successfully!")

        return super().form_valid(form) 

    def form_invalid(self, form):
        messages.error(self.request, "❌ There was an error processing your purchase. Please try again.")
        return self.render_to_response(self.get_context_data(form=form))
    
class Menu_item_create_view(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model=models.menu_item
    template_name='django_delights/menu_form.html'
    fields=['name', 'price', 'blerb']
    success_url=reverse_lazy('menu')
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser
class Menu_item_update_view(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model=models.menu_item
    template_name='django_delights/menu_update_form.html'
    fields=['name', 'price', 'blerb']
    success_url=reverse_lazy('menu')
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser
class Menu_item_delete_view(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=models.menu_item
    template_name = 'django_delights/menu_delete.html'
    success_url=reverse_lazy('menu')
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_superuser
class Menu_detail_view(LoginRequiredMixin, DetailView):
    model=models.menu_item
    template_name='django_delights/menu_detail.html'
    context_object_name='menu_item'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ingredient_list = models.recipe_item.objects.filter(dish=self.object)
        reviews_list = models.review.objects.filter(dish=self.object)
        total_cost = sum(ingredient.amount * ingredient.item.cost_per_unit for ingredient in ingredient_list)
        if not total_cost:
            total_cost = 0
        profit_per_dish = context['menu_item'].price - total_cost
        context['ingredients'] = ingredient_list
        context['total_cost'] = total_cost
        context['profit_per_dish'] = profit_per_dish
        context['review_list'] = reviews_list
        import pprint
        pprint.pprint(context)

        return context

class ingredient_view(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model=models.Ingredient
    template_name='django_delights/inventory.html'
    context_object_name='ingredient_list'
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser
class InventoryCreateUpdateView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'django_delights/inventory_form.html'
    form_class = forms.inventory_form
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser
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
class inventory_deleteview(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=models.Ingredient
    template_name='django_delights/inventory_delete.html'
    success_url='inventory'
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_superuser

class custom_loginview(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('index')
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

class recipe_item_createview(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model =models.recipe_item
    template_name = 'django_delights/recipe_form.html'
    form_class = forms.recipe_form
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser
    def form_valid(self, form):
        dish = get_object_or_404(models.menu_item, pk=self.kwargs["pk"])
        form.instance.dish = dish  # Set the recipe before saving
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("menu_detail", kwargs={"pk": self.kwargs["pk"]})
class recipe_update_view(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model=models.recipe_item
    template_name = 'django_delights/recipe_update.html'
    fields=['item', 'amount']
    login_url = 'login'
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser
    def get_success_url(self):
        return reverse("menu_detail", kwargs={"pk": self.object.dish.pk})
    
class recipe_delete_view(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=models.recipe_item
    template_name = 'django_delights/recipe_delete.html'
    login_url = 'login'
    def test_func(self):
        return self.request.user.is_superuser
    def get_success_url(self):
        return reverse("menu_detail", kwargs={"pk": self.object.dish.pk})    
class purchase_view(ListView):
    model=models.purchases
    template_name='django_delights/purchase_list.html'
    context_object_name='purchase_list'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchase_with_price = []
        grand_total_cost = 0
        grand_total_income =0
        grand_total_profit = 0

        for purchase in context['purchase_list']:
            menu_object = purchase.item
            total_price = menu_object.price * purchase.quantity
            ingredient_list = models.recipe_item.objects.filter(dish=menu_object)

            cost_per = sum(ingredient.amount * ingredient.item.cost_per_unit for ingredient in ingredient_list)
            total_cost = cost_per * purchase.quantity
            total_profit = total_price - total_cost
            purchase_with_price.append({'total_price':total_price, 'total_cost':total_cost, 'total_profit':total_profit,
                                        'menu_item': menu_object, 'quantity':purchase.quantity, 'purchase_object':purchase})
            context['purchase_with_price'] = purchase_with_price
            grand_total_cost += total_cost
            grand_total_profit += total_profit
            grand_total_income += total_price
        context['grand_total_cost'] = grand_total_cost
        context['grand_total_income'] = grand_total_income
        context['grand_total_profit'] = grand_total_profit
        return context
class purchase_update_view(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model=models.purchases
    template_name = 'django_delights/purchase_update.html'
    fields=['item', 'quantity']
    success_url=reverse_lazy('purchase_view')
    login_url = 'login'
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser
class purchase_delete_view(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=models.purchases
    template_name = 'django_delights/purchase_delete.html'
    success_url=reverse_lazy('purchases_view')
    login_url = 'login'
    def test_func(self):
        return self.request.user.is_superuser

class review_createview(LoginRequiredMixin, CreateView):
    model =models.review
    template_name = 'django_delights/review_form.html'
    form_class = forms.review_form
    login_url = 'login'

    def form_valid(self, form):
        dish = get_object_or_404(models.menu_item, pk=self.kwargs["pk"])
        form.instance.dish = dish
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("menu_detail", kwargs={"pk": self.kwargs["pk"]})
    
class review_updateview(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model=models.review
    template_name= 'django_delights/review_update.html'
    fields = ['text']
    login_url = 'login'

    def test_func(self):
        if self.request.user.is_superuser or self.request.user == self.get_object().user:
            return True
        else:
            return False
    def get_success_url(self):
        return reverse("menu_detail", kwargs={"pk": self.object.dish.pk})
    
class review_delete_view(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=models.review
    template_name = 'django_delights/review_delete.html'
    login_url = 'login'
    def test_func(self):
        if self.request.user.is_superuser or self.request.user == self.get_object().user:
            return True
        else:
            return False
    def get_success_url(self):
        return reverse("menu_detail", kwargs={"pk": self.object.dish.pk})   