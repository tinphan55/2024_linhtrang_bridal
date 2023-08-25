from django.db import models
from django.db.models import  Sum, F


class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Ward(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Client (models.Model):
    full_name = models.CharField(max_length= 50, verbose_name='Tên đầy đủ')
    code = models.CharField(max_length= 50, verbose_name='Mã KH')
    phone = models.IntegerField(null=False, verbose_name='Điện thoại', unique=True)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    last_order_date = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=100, null= True, blank = True, verbose_name='Địa chỉ')
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE,null= True, blank = True, verbose_name='Phường/Xã')
    birthday = models.DateField(null=True, blank = True, verbose_name='Ngày sinh')
    note =  models.CharField(max_length= 200,null=True, blank = True, verbose_name='Ghi chú')
    total_values = models.IntegerField (default=0)
    str_total_values = models.CharField(max_length= 100,null=True, blank = True, verbose_name='Tổng tiền mua')


    class Meta:
        verbose_name = 'Quản lí Khách hàng'
        verbose_name_plural = 'Quản lí Khách hàng'

    def __str__(self):
        return str(self.full_name) + '_' + str(self.code)
    
    def save(self, *args, **kwargs):
        if self.ward:
            self.address = str(self.ward)+ str(', ')+ str(self.ward.district) + str(', ')+ str(self.ward.district.province)
        super(Client , self).save(*args, **kwargs)

def update_ward_for_empty_records():
    clients_with_empty_ward = Client.objects.filter(ward__isnull=True, address__isnull=False)
    
    for client in clients_with_empty_ward:
        address = client.address
        matching_wards = Ward.objects.filter(name__icontains=address)
        
        if matching_wards.exists():
            ward = matching_wards.first()
            client.ward = ward
            client.save(update_fields=['ward'])