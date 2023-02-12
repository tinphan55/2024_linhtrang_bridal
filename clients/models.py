from django.db import models
from django.db.models import  Sum, F

class Client (models.Model):
    full_name = models.CharField(max_length= 50)
    code = models.CharField(max_length= 50)
    phone = models.IntegerField(null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    last_order_date = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=100, null= True, blank = True)
    birthday = models.DateField(null=True, blank = True)
    #total_values = models.IntegerField (default=0)

    def __str__(self):
        return str(self.full_name) + ' ' + str(self.code)
    

