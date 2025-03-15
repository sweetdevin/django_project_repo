from django.db import models

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

class user(models.Model):
    name = models.CharField(max_length=50)

class purchases(models.Model):
    item = models.ForeignKey(menu_item, on_delete=models.SET_DEFAULT, default='OLD MENU ITEM')
    time_stamp = models.DateTimeField()
    user = models.ForeignKey(user, on_delete=models.CASCADE)
