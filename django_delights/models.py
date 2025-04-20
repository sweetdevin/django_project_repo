from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=30)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    units_of_measure = models.CharField(max_length=50)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return self.name

class menu_item(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    blerb = models.TextField()

    def __str__(self):
        return self.name
class recipe_item(models.Model):
    dish = models.ForeignKey(menu_item, on_delete=models.CASCADE)
    item = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class purchases(models.Model):
    item = models.ForeignKey(menu_item, on_delete=models.SET_DEFAULT, default='OLD MENU ITEM')
    quantity = models.IntegerField()

class review(models.Model):
    dish = models.ForeignKey(menu_item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text= models.TextField()
    