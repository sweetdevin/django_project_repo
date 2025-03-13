from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from . import models

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