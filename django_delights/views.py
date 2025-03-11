from django.shortcuts import render
from django.views.generic import ListView
from . import models

# Create your views here.
def index(request):
    return render(request, 'django_delights/index.html')

class menu_view(ListView):
    model=models.menu_item
    template_name='django_delights/menu.html'
    context_object_name='menu_list'
