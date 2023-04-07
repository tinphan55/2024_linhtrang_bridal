from django.db import models
from order.models import Cart
from datetime import datetime
from django.db.models import Max
from django.core.exceptions import ValidationError



# Create your models here.
class Bill(models.Model):
    code = models.CharField(max_length=10, verbose_name="Mã hóa đơn")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    note = models.TextField(default= "", null = True, blank= True, verbose_name="Ghi chú")
    next_payment = models.DateField(null = True, blank= True, verbose_name="Ngày thanh toán kế tiếp")
    class Meta:
        verbose_name = 'Hóa đơn'
        verbose_name_plural = 'Hóa đơn'

      

    
    def __str__(self):
        month = datetime.now().month
        return str(self.id)+ "_" + str(month)
    
    
    
    

    

class BillItems(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Chọn Cart xuất hóa đơn'
        verbose_name_plural = 'Chọn Cart xuất hóa đơn'
