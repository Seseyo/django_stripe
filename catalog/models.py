from django.db import models

# Модель Item с полями (name, description, price)
class Item(models.Model):

    name = models.CharField(max_length=200, help_text="Enter a name of Item")
    description = models.CharField(max_length=200, help_text="Enter description")
    price = models.IntegerField(help_text="Example 2000 = 20$ 00cents")
#    currency = models

    def __str__(self):
        return self.name

'''
class Order(models.Model):
    
    item_id = models.ForeignKey('Item', on_delete=models.SET_NULL, null=True)
'''

