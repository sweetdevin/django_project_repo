from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Ingredient)
admin.site.register(models.menu_item)
admin.site.register(models.purchases)
admin.site.register(models.recipe_item)