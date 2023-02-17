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
      
    
    def save(self, *args, **kwargs):
            month = datetime.now().month
            latest_bill = Bill.objects.aggregate(Max("id"))["id__max"]
            latest_id = latest_bill + 1 if latest_bill else 1
            self.code =  str(latest_id) +"_"+ str(month) 
            super().save(*args, **kwargs)
        

    
    def __str__(self):
        return str(self.code) 
    
    
    
    

    

class BillItems(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
