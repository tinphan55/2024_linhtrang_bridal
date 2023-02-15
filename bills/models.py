from django.db import models
from order.models import Cart



# Create your models here.
class Bill(models.Model):
    code = models.CharField(max_length=10)
    created_date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(default= "Điền ghi chú tại đây")
    # incurred =  models.IntegerField(default=0)
    # total_retail  = models.IntegerField(default=0)
    # discount = models.IntegerField(default=0)
    # total= models.IntegerField(default=0)
    # paid = models.IntegerField(null= False, blank=False, default=0)
    # receivable = models.FloatField(default=0)
    # # external_url = models.CharField(max_length=200)

    
    def __str__(self):
        return str(self.code) 
    
    
    

    

class BillItems(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    # incurred =  models.IntegerField(default=0)
    # total  = models.IntegerField(default=0)
    # paid = models.IntegerField(null= False, blank=False, default=0)
    # receivable = models.FloatField(default=0)