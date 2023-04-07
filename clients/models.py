from django.db import models
from django.db.models import  Sum, F



class Client (models.Model):
    full_name = models.CharField(max_length= 50, verbose_name='Tên đầy đủ')
    code = models.CharField(max_length= 50, verbose_name='Mã KH')
    phone = models.IntegerField(null=False, verbose_name='Điện thoại')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    last_order_date = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=100, null= True, blank = True, verbose_name='Địa chỉ')
    birthday = models.DateField(null=True, blank = True, verbose_name='Ngày sinh')
    #total_values = models.IntegerField (default=0)

    class Meta:
        verbose_name = 'Quản lí Khách hàng'
        verbose_name_plural = 'Quản lí Khách hàng'

    def __str__(self):
        return str(self.full_name) + '_' + str(self.code)
    
    
