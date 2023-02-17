from django.db import models
from order.models import Cart
from datetime import datetime
from django.db.models import Max
from django.core.exceptions import ValidationError



# Create your models here.
class Bill(models.Model):
    code = models.CharField(max_length=10)
    created_date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(default= "", null = True, blank= True)
    next_payment = models.DateField(null = True, blank= True)
      
    

        

    
    def __str__(self):
        month = datetime.now().month
        return str(self.id)+ "_" + str(month)
    
    
    
    

    

class BillItems(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
