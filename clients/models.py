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
    code = models.CharField(max_length= 50,unique=False, verbose_name='Mã KH')
    phone = models.IntegerField(null=False, verbose_name='Điện thoại', unique=True)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    last_order_date = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=100, null= True, blank = True, verbose_name='Địa chỉ')
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE,verbose_name='Phường/Xã')
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

# def update_ward_for_empty_records():
#     clients_with_empty_ward = Client.objects.filter(ward__isnull=True, address__isnull=False)
    
#     for client in clients_with_empty_ward:
#         address = client.address
#         matching_wards = Ward.objects.filter(name__icontains=address)
        
#         if matching_wards.exists():
#             ward = matching_wards.first()
#             client.ward = ward
#             client.save(update_fields=['ward'])

def lookup_client_dulicate_phone( ):
    duplicate_phones = Client.objects.values('phone').annotate(phone_count=Count('phone')).filter(phone_count__gt=1)
    # Tạo danh sách chứa các khóa chính của các bản ghi có số điện thoại trùng nhau
    for entry in duplicate_phones:
        phone = entry['phone']
        records = Client.objects.filter(phone=phone)
        best_client = records.order_by('-total_values').first()
        if best_client:
            new_queryset = records.exclude(pk=best_client.pk)
            for client in new_queryset:
                carts = Cart.objects.filter(client=client.pk)
                for cart in carts:
                    cart.client = best_client
                    cart.save()
            for item in new_queryset:
                item.delete()
            
        
def update_ward(text, name_ward):
    text = text.lower()
    try:
        # Lấy đối tượng Ward dựa trên tên
        ward_instance = Ward.objects.filter(name__icontains=name_ward)
        clients_with_empty_ward = Client.objects.filter(ward__isnull=True, address=text)
        for client in clients_with_empty_ward:
            client.ward = ward_instance[0]
            client.save()
    except Ward.DoesNotExist:
        print('không có phường')

        
    