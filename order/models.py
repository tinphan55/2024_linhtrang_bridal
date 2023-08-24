# Create your models here.
from decimal import Decimal
from django.db import models
from clients.models import Client
from django.contrib.auth.models import User
from datetime import datetime
from services_admin.models import *
from django.dispatch import receiver
from django.db.models import  Sum, F
from datetime import datetime, timedelta, date
from django.conf import settings
from itertools import chain
from django.db.models import Max
from django.db.models.signals import post_save, post_delete,pre_save
from telegram import Bot
from infobot import *
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError





class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True, blank= True, 
                             verbose_name="Người tạo")
    user_modified = models.CharField(max_length=150, blank=True, null=True,
                             verbose_name="Người chỉnh sửa")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, 
                               verbose_name="KH")
    created_at = models.DateTimeField(default=datetime.now, verbose_name="Ngày tạo")
    wedding_date= models.DateField(null=False, blank= False, verbose_name="Ngày cưới 1")
    wedding_date_2= models.DateField(null=True, blank= True, verbose_name="Ngày cưới 2")
    note = models.TextField(max_length=500, null= True, blank=True, verbose_name="Ghi chú")
    incurred = models.IntegerField(null= True, blank=True, default=0, verbose_name="Phát sinh")
    total_price = models.FloatField(default=0, verbose_name='Tổng tiền')
    total_bill = models.FloatField(default=0)
    paid = models.IntegerField(null= False, blank=False, default=0)
    str_receivable = models.CharField(max_length=50,null= True, blank=True, verbose_name="Cần thu")
    total_clothe= models.FloatField(default=0, verbose_name='Doanh thu Đồ cưới')
    total_photo= models.FloatField(default=0, verbose_name='Doanh thu chụp hình')
    total_makup = models.FloatField(default=0, verbose_name='Doanh thu trang điểm')
    total_accessory_hr = models.FloatField(default=0, verbose_name='Doanh thu phụ kiện tính lương')
    total_accessory = models.FloatField(default=0, verbose_name='Doanh thu phụ kiện')
    str_total_clothe =  models.CharField(max_length=50,null= True, blank=True, verbose_name="Doanh thu Đồ cưới")
    str_total_makup =models.CharField(max_length=50,null= True, blank=True, verbose_name="Doanh thu trang điểm")
    str_total_accessory =models.CharField(max_length=50,null= True, blank=True, verbose_name="Doanh thu phụ kiện")
    str_total_photo =models.CharField(max_length=50,null= True, blank=True, verbose_name="Doanh thu chụp hình")
    total_discount_raw = models.FloatField(default=0, verbose_name='Giảm giá')
    total_cart_raw = models.FloatField(default=0, verbose_name='Tổng doanh thu')
    total_incurred_raw = models.FloatField(default=0, verbose_name='Tổng phát sinh')
    total_payment_raw = models.FloatField(default=0, verbose_name='Tổng đã trả')
    total_raw = models.FloatField(default=0, verbose_name='Tổng tiền')
    str_total_raw =  models.CharField(max_length=50,null= True, blank=True, verbose_name="Tổng tiền")
    receivable_raw  = models.FloatField(default=0, verbose_name='Cần thu')
    total_deposit_raw =  models.FloatField(default=0, verbose_name='Cần đặt cọc')
    discount_clothe= models.FloatField(default=0)
    discount_photo= models.FloatField(default=0)
    discount_makup= models.FloatField(default=0)
    discount_accessory= models.FloatField(default=0)
    deposit_clothe= models.FloatField(default=0)
    deposit_photo= models.FloatField(default=0)
    deposit_makup= models.FloatField(default=0)
    deposit_accessory= models.FloatField(default=0)
    str_total_cart = models.CharField(max_length=50,null= True, blank=True, verbose_name="Tổng trước giảm")
    str_total_incurred= models.CharField(max_length=50,null= True, blank=True, verbose_name="Tổng phát sinh")
    str_total_discount = models.CharField(max_length=50,null= True, blank=True, verbose_name="Tổng giảm")
    str_total =models.CharField(max_length=50,null= True, blank=True, verbose_name="Tổng sau giảm")
    str_total_payment  =models.CharField(max_length=50,null= True, blank=True, verbose_name="Tổng trả")
    str_total_deposit =models.CharField(max_length=50,null= True, blank=True, verbose_name="Cần đặt cọc")



    def __str__(self):
        return str(self.id) + '_' + str(self.client) 
    
    def return_id_cart(self):
        return self.id
    

    def save(self, *args, **kwargs):
        self.total_discount_raw = self.discount_clothe + self.discount_photo + self.discount_makup + self.discount_accessory
        self.total_deposit_raw = self.deposit_clothe + self.deposit_photo + self.deposit_makup +self.deposit_accessory
        #doanh thu trước giảm giá
        self.total_cart_raw = self.total_clothe + self.total_photo + self.total_makup +self.total_accessory +self.total_discount_raw
        self.str_total_cart = '{:,.0f}'.format(self.total_cart_raw)
        #doanh thu sau giảm giá
        self.total_raw = self.total_cart_raw + self.total_incurred_raw - self.total_discount_raw
        self.str_total = '{:,.0f}'.format(self.total_raw)
        self.receivable_raw = self.total_raw - self.total_payment_raw
        self.str_total_incurred='{:,.0f}'.format(self.total_incurred_raw)
        self.str_total_discount = '{:,.0f}'.format(self.total_discount_raw)
        self.str_total_payment= '{:,.0f}'.format(self.total_payment_raw)
        self.str_receivable = '{:,.0f}'.format(self.receivable_raw)
        self.str_total_deposit = '{:,.0f}'.format(self.total_deposit_raw)
        super(Cart, self).save(*args, **kwargs)
    
    @property
    def latest_paid(self):
        latest_payment = PaymentScheduleCart.objects.filter(cart=self).aggregate(Max('created_at'))
        return latest_payment['created_at__max']
    
        
class CartItems(models.Model):
    class Meta:
        abstract = True
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(default=datetime.now)
    price = models.FloatField(blank=True, default=0, verbose_name="Giá")
    qty = models.IntegerField(default=1, verbose_name="Số lượng")
    discount = models.IntegerField(null= True, blank=True, default=0,verbose_name= "Giảm giá")
    is_discount = models.BooleanField(default=False, verbose_name="Có giảm giá")  
    total_items = models.IntegerField(default=0, verbose_name="Tổng tiền")
    str_total_items = models.CharField(max_length=50,null= True, blank=True, verbose_name="Tổng tiền")
    str_price = models.CharField(max_length=50,null= True, blank=True, verbose_name="Giá")
    str_discount = models.CharField(max_length=50,null= True, blank=True, verbose_name="Giảm giá")
    total_deposit  = models.IntegerField(default=0,null= True, blank=True, verbose_name="Tổng đặt cọc")
    total_deposit_str = models.CharField(max_length=50,null= True, blank=True, verbose_name="Tổng đặt cọc")


    
class ClotheService(CartItems):
    clothe = models.ForeignKey(Clothe, on_delete = models.CASCADE,
     limit_choices_to={'is_available': True}, verbose_name='Trang phục')
    delivery_date = models.DateField(null= True, blank=True, verbose_name="Ngày giao")
    return_date = models.DateField(null= True, blank=True, verbose_name="Ngày hẹn trả")
    is_returned = models.BooleanField(default=False, verbose_name="Đã trả") 
    returned_at = models.DateTimeField(null=True, blank=True,verbose_name= "Ngày trả")  
    note = models.TextField(max_length=500, null = True, blank=True, verbose_name="Ghi chú")
    noti = models.CharField (max_length=200, verbose_name='Thông báo')
    # item_status  = models.CharField(max_length=50,null= True, blank=True, verbose_name="Trạng thái")
    previous_clothe_id = models.PositiveIntegerField(null=True, blank=True)
    previous_clothe_qty = models.PositiveIntegerField(default=0,null=True, blank=True)
    
    class Meta:
        # Đảm bảo rằng trong cùng một cart, chỉ có một clothe có id duy nhất được tạo
        unique_together = ('cart', 'clothe')
        verbose_name = 'Cho thuê đồ cưới'
        verbose_name_plural = 'Cho thuê đồ cưới'
        
    def clean(self):
        existing_service = ClotheService.objects.filter(cart=self.cart, clothe=self.clothe).exclude(pk=self.pk)
        if existing_service.exists():
            raise ValidationError(_("Bạn chỉ được chọn 1 mã áo cho 1 Cart"))

    
    
        
    def __str__(self):
        return str(self.clothe)
    
    def __init__(self, *args, **kwargs):
        super(ClotheService, self).__init__(*args, **kwargs)
        self._original_qty = self.qty  # Lưu giá trị qty ban đầu
        self._original_clothe_id = self.clothe_id  # Lưu giá trị clothe_id ban đầu
    
    
    @property
    def item_status(self):
        today = date.today()
        if today < self.delivery_date:
            status = "Chờ cho thuê"
        elif today >= self.delivery_date and self.returned_at is None:
            if today <= self.return_date:
                status = "Đang cho thuê"
            elif today > self.return_date:
                num_date = today - self.return_date
                status = f"QUÁ HẠN THUÊ {num_date.days} NGÀY"
        else:
            status = "Đã thu hồi"
        return status
    
    def save(self, *args, **kwargs):
        self.price = self.clothe.price
        self.str_price='{:,.0f}'.format(self.price)
        if self.is_discount:
            self.discount = self.clothe.ranking.discount * self.qty
        else:
            self.discount = 0
        self.str_discount='{:,.0f}'.format(self.discount)
        total = self.price*self.qty
        if total is None:
            total = 0
        else:
            total = total - self.discount
        self.total_items = total
        self.str_total_items='{:,.0f}'.format(self.total_items)
        INFINITY_DATE = date.max
        MINUS_INFINITY_DATE = date.min
        max_wedding_date = max(self.cart.wedding_date or MINUS_INFINITY_DATE,self.cart.wedding_date_2 or MINUS_INFINITY_DATE)
        min_wedding_date = min(self.cart.wedding_date or INFINITY_DATE, self.cart.wedding_date_2 or INFINITY_DATE)
        #     # max_date = max(wedding_date or MINUS_INFINITY_DATE, wedding_date2 or MINUS_INFINITY_DATE)
        if self.delivery_date == None:
            self.delivery_date = min_wedding_date - timedelta(days=2)
        if self.return_date == None:
            self.return_date = max_wedding_date + timedelta(days=2) 
        total_deposit = self.clothe.deposit* self.qty
        if total_deposit is None:
            self.total_deposit=0
        else:
            self.total_deposit =total_deposit
        self.total_deposit_str  ='{:,.0f}'.format( self.total_deposit)
        if self.qty != self._original_qty:
            self.previous_clothe_qty = self._original_qty  # Lưu qty cũ
        if self.clothe_id != self._original_clothe_id:
            self.previous_clothe_id = self._original_clothe_id  # Lưu clothe_id cũ
           
        
        super(ClotheService, self).save(*args, **kwargs)
        # Cập nhật giá trị ban đầu sau khi đã lưu
        self._original_qty = self.qty
        self._original_clothe_id = self.clothe_id
        

    

class PhotoService(CartItems):
    package = models.ForeignKey(Photo, on_delete = models.CASCADE, 
        limit_choices_to={'is_available': True}, verbose_name='Gói chụp')
    note = models.TextField(max_length=500, null= True, blank=True, 
                            verbose_name="Ghi chú")
    class Meta:
        verbose_name = 'Chụp hình'
        verbose_name_plural = 'Chụp hình'
    def __str__(self):
        return str(self.package)

    def save(self, *args, **kwargs):
        self.price = self.package.price
        self.str_price='{:,.0f}'.format(self.price)
        if self.is_discount == True:
            self.discount = self.package.discount* self.qty
        else:
            self.discount = 0
        self.str_discount='{:,.0f}'.format(self.discount)
        total = self.price*self.qty
        if total is None:
            total = 0
        else:
            total = total - self.discount
        self.total_items = total
        self.str_total_items='{:,.0f}'.format(self.total_items)
        total_deposit = self.package.deposit*self.qty
        if total_deposit is None:
            self.total_deposit=0
        else:
            self.total_deposit =total_deposit
        self.total_deposit_str  ='{:,.0f}'.format( self.total_deposit)
        super(PhotoService, self).save(*args, **kwargs)
   
    
class MakeupService(CartItems):
    package = models.ForeignKey(Makeup, on_delete = models.CASCADE, 
        limit_choices_to={'is_available': True}, verbose_name='Gói trang điểm')
    note = models.TextField(max_length=500, null= True, blank=True, verbose_name="Ghi chú")
    class Meta:
        verbose_name = 'Trang điểm'
        verbose_name_plural = 'Trang điểm'
    def save(self, *args, **kwargs):
        self.price = self.package.price
        self.str_price='{:,.0f}'.format(self.price)
        if self.is_discount == True:
             self.discount = self.package.discount* self.qty
        else:
            self.discount = 0
        self.str_discount='{:,.0f}'.format(self.discount)
        total = self.price*self.qty
        if total is None:
            total = 0
        else:
            total = total - self.discount
        self.total_items = total
        self.str_total_items='{:,.0f}'.format(self.total_items)
        total_deposit = self.package.deposit*self.qty
        if total_deposit is None:
            self.total_deposit= 0
        else:
            self.total_deposit = total_deposit
        self.total_deposit_str  ='{:,.0f}'.format( self.total_deposit)
        super(MakeupService, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.package)
 

class AccessorysSerive (CartItems):
    product = models.ForeignKey(Accessory, on_delete = models.CASCADE, 
        limit_choices_to={'is_available': True}, verbose_name='Sản phẩm')
    delivery_date = models.DateField(null= True, blank=True, verbose_name='Ngày giao')
    return_date = models.DateField(null= True, blank=True,verbose_name= "Ngày hẹn trả")
    is_returned = models.BooleanField(default=False, verbose_name="Đã trả") 
    returned_at = models.DateTimeField(null=True, blank=True, verbose_name="Ngày trả")  
    note = models.TextField(max_length=500, null = True, blank=True, verbose_name="Ghi chú")
    noti = models.CharField (max_length=200, null = True, blank=True)
    # item_status  = models.CharField(max_length=50,null= True, blank=True, verbose_name="Trạng thái")
    def __str__(self):
        return str(self.product)
    class Meta:
        verbose_name = 'Phụ kiện'
        verbose_name_plural = 'Phụ kiện'
    
    @property
    def item_status(self):
        today = date.today()
        if today < self.delivery_date:
            status = "Chờ cho thuê"
        elif today >= self.delivery_date and self.returned_at is None:
            if today <= self.return_date:
                status = "Đang cho thuê"
            elif today > self.return_date:
                num_date = today - self.return_date
                status = f"QUÁ HẠN THUÊ {num_date.days} NGÀY"
        else:
            status = "Đã thu hồi"
        return status
    
    def save(self, *args, **kwargs):
        self.price = self.product.price
        self.str_price='{:,.0f}'.format(self.price)
        INFINITY_DATE = date.max
        MINUS_INFINITY_DATE = date.min
        max_wedding_date = max(self.cart.wedding_date or MINUS_INFINITY_DATE,self.cart.wedding_date_2 or MINUS_INFINITY_DATE)
        min_wedding_date = min(self.cart.wedding_date or INFINITY_DATE, self.cart.wedding_date_2 or INFINITY_DATE)
        if self.is_discount == True:
             self.discount = self.product.discount * self.qty
        else:
            self.discount = 0
        self.str_discount='{:,.0f}'.format(self.discount)
        total = self.price*self.qty
        if total is None:
            total = 0
        else:
            total = total - self.discount
        self.total_items = total
        self.str_total_items='{:,.0f}'.format(self.total_items)
        if self.delivery_date == None:
            self.delivery_date = min_wedding_date - timedelta(days=2)
        if self.return_date == None:
            self.return_date = max_wedding_date + timedelta(days=2) 
        total_deposit = self.product.deposit*self.qty
        if total_deposit is None:
            self.total_deposit=0
        else:
            self.total_deposit =total_deposit
        self.total_deposit_str  ='{:,.0f}'.format( self.total_deposit)
        super(AccessorysSerive, self).save(*args, **kwargs)
    
    
class IncurredCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  
    description = models.TextField(max_length=500, null=False, verbose_name="Mô tả")
    created_at = models.DateTimeField(default=datetime.now, verbose_name="Ngày tạo")
    amount =  models.IntegerField(null= False, default=0, verbose_name="Số tiền")
    class Meta:
        verbose_name = 'Tiền phát sinh'
        verbose_name_plural = 'Tiền phát sinh'
    def __str__(self):
        return str(self.cart)
    
    
class PaymentScheduleCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  
    amount =  models.IntegerField(null= False, default=0, verbose_name="Số tiền")
    description = models.TextField(max_length=500, verbose_name='Mô tả')
    created_at = models.DateTimeField(default=datetime.now, verbose_name="Ngày tạo")
    class Meta:
        verbose_name = 'Khách trả tiền'
        verbose_name_plural = 'Khách trả tiền'
   
    def __str__(self):
        return str(self.cart)
    

class ReturnClothe(ClotheService):
    class Meta:
        proxy = True
        verbose_name = 'Quản lí trả đồ thuê cưới'
        verbose_name_plural = 'Quản lí trả đồ thuê cưới'

    def __str__(self):
        return str(self.clothe.code)
    
    
        

class ReturnAccessory (AccessorysSerive):
    class Meta:
        proxy = True
        verbose_name = 'Quản lí phụ kiện'
        verbose_name_plural = 'Quản lí phụ kiện'
    def get_queryset(self):
        return super().get_queryset().filter(product__is_sell=False)
    def __str__(self):
        return str(self.product.name)
    
class ClotheRentalInfo(models.Model):
    clothe = models.ForeignKey(Clothe, on_delete=models.CASCADE)
    rental_date = models.DateField()
    qty = models.PositiveIntegerField(default=1)
    available_qty = models.PositiveIntegerField(null=True, blank=True)
    class Meta:
        unique_together = ( 'clothe', 'rental_date')
    def __str__(self):
        return str(self.clothe.code)+str('_')+str(self.rental_date)


# @receiver(pre_save, sender=ClotheService)
# def update_previous_clothe_id(sender, instance, **kwargs):
#     try:
#         # Lấy ClotheService trước đó (nếu có)
#         previous_instance = ClotheService.objects.get(pk=instance.pk)
#         if previous_instance.clothe != instance.clothe:
#             instance.previous_clothe_id = previous_instance.clothe_id
#     except ClotheService.DoesNotExist:
#         pass  # Đối tượng mới được tạo, không cần xử lý 





@receiver([post_save, post_delete], sender=ClotheService)
def update_clothe_rental_info(sender, instance, **kwargs):
    created = kwargs.get('created', False)
    cart = instance.cart
    cart.total_clothe  = ClotheService.objects.filter(cart=cart).aggregate(models.Sum('total_items'))['total_items__sum'] or 0
    cart.str_total_clothe= '{:,.0f}'.format(cart.total_clothe)
    cart.discount_clothe =  ClotheService.objects.filter(cart=cart).aggregate(models.Sum('discount'))['discount__sum'] or 0
    cart.deposit_clothe = ClotheService.objects.filter(cart=cart).aggregate(models.Sum('total_deposit'))['total_deposit__sum'] or 0
    cart.save()
    if instance.clothe.is_available:  # Chỉ xử lý nếu Clothe có sẵn
        delivery_start_date = instance.delivery_date 
        return_end_date = instance.return_date 
        inital_qty = instance.clothe.qty
        
        rental_dates = []
        current_date = delivery_start_date
        
        while current_date <= return_end_date:
            rental_dates.append(current_date)
            current_date += timedelta(days=1)
        
        existing_rental_info = ClotheRentalInfo.objects.filter(clothe=instance.clothe, rental_date__in=rental_dates)
        existing_rental_info.delete()
        
        # Lấy previous_clothe_id
        previous_clothe_id = instance.previous_clothe_id
        
        for date in rental_dates:
            # Tính toán tổng số lượng cho mỗi ngày thuê cho Clothe
            total_rental_qty = ClotheService.objects.filter(
                clothe = instance.clothe,  # Sử dụng previous_clothe_id
                delivery_date__lte=date,
                return_date__gte=date
            ).aggregate(total_qty=Sum('qty'))['total_qty'] or 0
            avai_qty = max(inital_qty - total_rental_qty, 0)
            # Tạo hoặc cập nhật thông tin thuê cho Clothe mới
            ClotheRentalInfo.objects.create(
                clothe=instance.clothe,
                rental_date=date,
                qty = total_rental_qty,
                available_qty = avai_qty

                )
            old_clothe = ClotheRentalInfo.objects.filter(rental_date=date, clothe=previous_clothe_id).first()
            if old_clothe:
                if not created and previous_clothe_id != instance.pk:  
                    if  previous_clothe_id:  
                        if instance.previous_clothe_qty==0 or previous_clothe_id is None or instance.previous_clothe_qty != instance.qty :
                                new_qty = old_clothe.qty - instance.qty
                        else:
                                new_qty = old_clothe.qty - instance.previous_clothe_qty
                    
                if new_qty <0:
                    new_qty = 0
                ClotheRentalInfo.objects.update_or_create(
                                    rental_date=date,  
                                    clothe=previous_clothe_id,
                                    defaults={
                                        'qty': new_qty,
                                        'available_qty': inital_qty - new_qty}
                                )
            


        


# Nếu đổi ngày cưới phải vào lại chọn áo
# @receiver(post_save, sender=Cart)
# def update_manage_clothe(sender, instance, created, **kwargs):
#     if not created:
#         if instance.pk:  # Check if instance is already saved (updating)
#             original_instance = Cart.objects.get(pk=instance.pk)
#             if instance.wedding_date != original_instance.wedding_date or instance.wedding_date_2 != original_instance.wedding_date_2  :
#                 INFINITY_DATE = date.max
#                 MINUS_INFINITY_DATE = date.min
#                 max_wedding_date = max(instance.wedding_date or MINUS_INFINITY_DATE,instance.wedding_date_2 or MINUS_INFINITY_DATE)
#                 min_wedding_date = min(instance.wedding_date or INFINITY_DATE, instance.wedding_date_2 or INFINITY_DATE)
#                 clothe = ClotheService.objects.filter(cart = instance.pk)
#                 accessory = AccessorysSerive.objects.filter(cart = instance.pk)
#                 for item in clothe:
#                     item.delivery_date = min_wedding_date - timedelta(days=2)
#                     item.return_date = max_wedding_date + timedelta(days=2)
#                     item.save()
#                 for item in accessory:
#                     item.delivery_date = min_wedding_date - timedelta(days=2)
#                     item.return_date = max_wedding_date + timedelta(days=2)
#                     item.save()


@receiver(post_save, sender=Cart)
def send_cart_message(sender, instance, created, **kwargs):
    if created:
        bot = Bot(token= bot_truong)
        bot.send_message(
                chat_id= chat_group_id, 
                text= f"Có Cart mới,tạo bởi {instance.user}, ngày cưới là {instance.wedding_date}") 

@receiver(post_delete, sender=PaymentScheduleCart)
def send_payment_message_on_delete(sender, instance, **kwargs):
    bot = Bot(token=bot_truong)
    text = f"[CẢNH BÁO] Thông tin thanh toán với số tiền {'{:,.0f}'.format(instance.amount)} của cart {instance.cart} đã bị xóa khỏi lịch thanh toán"
    bot.send_message(chat_id=chat_group_id, text=text)

@receiver(post_save, sender=PaymentScheduleCart)
def send_payment_message_on_save(sender, instance, created, **kwargs):
    bot = Bot(token=bot_truong)
    if created:
        text = f"Tiền vô, thêm {'{:,.0f}'.format(instance.amount)} đồng, được cập nhật bởi {instance.cart.user} cho cart {instance.cart}"
    else:
        text = f"[CẢNH BÁO] Thông tin thanh toán với số tiền {'{:,.0f}'.format(instance.amount)} của cart {instance.cart} đã được chỉnh sửa"
    bot.send_message(chat_id=chat_group_id, text=text)




# @receiver(post_save, sender=ClotheService)
# def update_total_clothe(sender, instance, created, **kwargs):
#             cart = instance.cart
#             cart.total_clothe  = ClotheService.objects.filter(cart=cart).aggregate(models.Sum('total_items'))['total_items__sum'] or 0
#             cart.str_total_clothe= '{:,.0f}'.format(cart.total_clothe)
#             cart.discount_clothe =  ClotheService.objects.filter(cart=cart).aggregate(models.Sum('discount'))['discount__sum'] or 0
#             cart.deposit_clothe = ClotheService.objects.filter(cart=cart).aggregate(models.Sum('total_deposit'))['total_deposit__sum'] or 0
#             cart.save()
@receiver([post_save, post_delete],  sender=PhotoService)  
def update_total_photo(sender, instance, **kwargs):
            created = kwargs.get('created', False)
            cart = instance.cart
            cart.total_photo = PhotoService.objects.filter(cart=cart).aggregate(models.Sum('total_items'))['total_items__sum'] or 0
            cart.str_total_photo= '{:,.0f}'.format(cart.total_photo)
            cart.discount_photo =  PhotoService.objects.filter(cart=cart).aggregate(models.Sum('discount'))['discount__sum'] or 0
            cart.deposit_photo = PhotoService.objects.filter(cart=cart).aggregate(models.Sum('total_deposit'))['total_deposit__sum'] or 0
            cart.save()

@receiver([post_save, post_delete], sender=MakeupService)
def update_total_makup(sender, instance,  **kwargs):
            created = kwargs.get('created', False)
            cart = instance.cart
            cart.total_makup = MakeupService.objects.filter(cart=cart).aggregate(models.Sum('total_items'))['total_items__sum'] or 0
            cart.str_total_makup= '{:,.0f}'.format(cart.total_makup)
            cart.discount_makup =  MakeupService.objects.filter(cart=cart).aggregate(models.Sum('discount'))['discount__sum'] or 0
            cart.deposit_makup = MakeupService.objects.filter(cart=cart).aggregate(models.Sum('total_deposit'))['total_deposit__sum'] or 0
            cart.save()
    
@receiver([post_save, post_delete],  sender=AccessorysSerive)
def update_total_accessorys(sender, instance,**kwargs):
            created = kwargs.get('created', False)
            cart = instance.cart
            cart.total_accessory = AccessorysSerive.objects.filter(cart=cart).aggregate(models.Sum('total_items'))['total_items__sum'] or 0
            cart.total_accessory_hr = AccessorysSerive.objects.filter(cart=cart,product__is_hr = True).aggregate(models.Sum('total_items'))['total_items__sum'] or 0
            cart.str_total_accessory= '{:,.0f}'.format(cart.total_accessory)
            cart.discount_accessory =  AccessorysSerive.objects.filter(cart=cart).aggregate(models.Sum('discount'))['discount__sum'] or 0
            cart.deposit_accessory = AccessorysSerive.objects.filter(cart=cart).aggregate(models.Sum('total_deposit'))['total_deposit__sum'] or 0
            cart.save()    

@receiver([post_save, post_delete],  sender=IncurredCart)
def update_total_incurred(sender, instance, **kwargs):
    created = kwargs.get('created', False)
    cart = instance.cart
    cart.total_incurred_raw =IncurredCart.objects.filter(cart=cart).aggregate(models.Sum('amount'))['amount__sum'] or 0 
    cart.save()
 
@receiver([post_save, post_delete],  sender=PaymentScheduleCart)
def update_total_payment(sender, instance,  **kwargs):
    created = kwargs.get('created', False)
    cart = instance.cart
    cart.total_payment_raw =PaymentScheduleCart.objects.filter(cart=cart).aggregate(models.Sum('amount'))['amount__sum'] or 0 
    cart.save()   

  
def save_clothe():
    clothe = ClotheService.objects.all()
    for self in clothe:
        self.price = self.clothe.price
        self.str_price='{:,.0f}'.format(self.price)
        if self.is_discount:
            self.discount = self.clothe.ranking.discount * self.qty
        else:
            self.discount = 0
        self.str_discount='{:,.0f}'.format(self.discount)
        total = self.price*self.qty
        if total is None:
            total = 0
        else:
            total = total - self.discount
        self.total_items = total
        self.str_total_items='{:,.0f}'.format(self.total_items)
        INFINITY_DATE = date.max
        MINUS_INFINITY_DATE = date.min
        max_wedding_date = max(self.cart.wedding_date or MINUS_INFINITY_DATE,self.cart.wedding_date_2 or MINUS_INFINITY_DATE)
        min_wedding_date = min(self.cart.wedding_date or INFINITY_DATE, self.cart.wedding_date_2 or INFINITY_DATE)
        #     # max_date = max(wedding_date or MINUS_INFINITY_DATE, wedding_date2 or MINUS_INFINITY_DATE)
        if self.delivery_date == None:
            self.delivery_date = min_wedding_date - timedelta(days=2)
        if self.return_date == None:
            self.return_date = max_wedding_date + timedelta(days=2) 
        self.total_deposit = self.clothe.deposit* self.qty
        self.save()

def save_photo():
    photo = PhotoService.objects.all()
    for self in photo:
        self.price = self.package.price
        self.str_price='{:,.0f}'.format(self.price)
        if self.is_discount == True:
            self.discount = self.package.discount* self.qty
        else:
            self.discount = 0
        self.str_discount='{:,.0f}'.format(self.discount)
        total = self.price*self.qty
        if total is None:
            total = 0
        else:
            total = total - self.discount
        self.total_items = total
        self.str_total_items='{:,.0f}'.format(self.total_items)
        total_deposit = self.package.deposit*self.qty
        if total_deposit is None:
            self.total_deposit=0
        else:
            self.total_deposit =total_deposit
        self.save()

def save_makup():
    makup = MakeupService.objects.all()
    for self in makup:
        self.price = self.package.price
        self.str_price='{:,.0f}'.format(self.price)
        if self.is_discount == True:
             self.discount = self.package.discount* self.qty
        else:
            self.discount = 0
        self.str_discount='{:,.0f}'.format(self.discount)
        total = self.price*self.qty
        if total is None:
            total = 0
        else:
            total = total - self.discount
        self.total_items = total
        self.str_total_items='{:,.0f}'.format(self.total_items)
        total_deposit = self.package.deposit*self.qty
        if total_deposit is None:
            self.total_deposit= 0
        else:
            self.total_deposit = total_deposit
        self.save()

def save_acc():
    acc = AccessorysSerive.objects.all()
    for self in acc:
        self.price = self.product.price
        self.str_price='{:,.0f}'.format(self.price)
        INFINITY_DATE = date.max
        MINUS_INFINITY_DATE = date.min
        max_wedding_date = max(self.cart.wedding_date or MINUS_INFINITY_DATE,self.cart.wedding_date_2 or MINUS_INFINITY_DATE)
        min_wedding_date = min(self.cart.wedding_date or INFINITY_DATE, self.cart.wedding_date_2 or INFINITY_DATE)
        if self.is_discount == True:
             self.discount = self.product.discount * self.qty
        else:
            self.discount = 0
        self.str_discount='{:,.0f}'.format(self.discount)
        total = self.price*self.qty
        if total is None:
            total = 0
        else:
            total = total - self.discount
        self.total_items = total
        self.str_total_items='{:,.0f}'.format(self.total_items)
        if self.delivery_date == None:
            self.delivery_date = min_wedding_date - timedelta(days=2)
        if self.return_date == None:
            self.return_date = max_wedding_date + timedelta(days=2) 
        total_deposit = self.product.deposit*self.qty
        if total_deposit is None:
            self.total_deposit=0
        else:
            self.total_deposit =total_deposit
        self.save()

def save_car():
    carts = Cart.objects.all()
    for cart in carts:
        cart.total_clothe  = ClotheService.objects.filter(cart=cart).aggregate(models.Sum('total_items'))['total_items__sum'] or 0
        cart.str_total_clothe= '{:,.0f}'.format(cart.total_clothe)
        cart.discount_clothe =  ClotheService.objects.filter(cart=cart).aggregate(models.Sum('discount'))['discount__sum'] or 0
        cart.deposit_clothe = ClotheService.objects.filter(cart=cart).aggregate(models.Sum('total_deposit'))['total_deposit__sum'] or 0
        cart.total_photo = PhotoService.objects.filter(cart=cart).aggregate(models.Sum('total_items'))['total_items__sum'] or 0
        cart.str_total_photo= '{:,.0f}'.format(cart.total_photo)
        cart.discount_photo =  PhotoService.objects.filter(cart=cart).aggregate(models.Sum('discount'))['discount__sum'] or 0
        cart.deposit_photo = PhotoService.objects.filter(cart=cart).aggregate(models.Sum('total_deposit'))['total_deposit__sum'] or 0
        cart.total_makup = MakeupService.objects.filter(cart=cart).aggregate(models.Sum('total_items'))['total_items__sum'] or 0
        cart.str_total_makup= '{:,.0f}'.format(cart.total_makup)
        cart.discount_photo =  MakeupService.objects.filter(cart=cart).aggregate(models.Sum('discount'))['discount__sum'] or 0
        cart.deposit_makup = MakeupService.objects.filter(cart=cart).aggregate(models.Sum('total_deposit'))['total_deposit__sum'] or 0
        cart.total_accessory = AccessorysSerive.objects.filter(cart=cart).aggregate(models.Sum('total_items'))['total_items__sum'] or 0
        cart.total_accessory_hr = AccessorysSerive.objects.filter(cart=cart,product__is_hr = True).aggregate(models.Sum('total_items'))['total_items__sum'] or 0
        cart.str_total_accessory= '{:,.0f}'.format(cart.total_accessory)
        cart.discount_accessory =  AccessorysSerive.objects.filter(cart=cart).aggregate(models.Sum('discount'))['discount__sum'] or 0
        cart.deposit_accessory = AccessorysSerive.objects.filter(cart=cart).aggregate(models.Sum('total_deposit'))['total_deposit__sum'] or 0
        cart.total_incurred_raw =IncurredCart.objects.filter(cart=cart).aggregate(models.Sum('amount'))['amount__sum'] or 0 
        cart.total_payment_raw =PaymentScheduleCart.objects.filter(cart=cart).aggregate(models.Sum('amount'))['amount__sum'] or 0 
        cart.save()


def save_clothe_info_rent ():
    clothes = ClotheService.objects.all()
    for instance in clothes:
            delivery_start_date = instance.delivery_date 
            return_end_date = instance.return_date 
            inital_qty = instance.clothe.qty
            rental_dates = []
            current_date = delivery_start_date
            while current_date <= return_end_date:
                rental_dates.append(current_date)
                current_date += timedelta(days=1)
            existing_rental_info = ClotheRentalInfo.objects.filter(clothe=instance.clothe, rental_date__in=rental_dates)
            existing_rental_info.delete()
            # Lấy previous_clothe_id
            previous_clothe_id = instance.previous_clothe_id
            for date in rental_dates:
                # Tính toán tổng số lượng cho mỗi ngày thuê cho Clothe
                total_rental_qty = ClotheService.objects.filter(
                    clothe = instance.clothe,  # Sử dụng previous_clothe_id
                    delivery_date__lte=date,
                    return_date__gte=date
                ).aggregate(total_qty=Sum('qty'))['total_qty'] or 0
                avai_qty = max(inital_qty - total_rental_qty, 0)
                # Tạo hoặc cập nhật thông tin thuê cho Clothe mới
                ClotheRentalInfo.objects.create(
                    clothe=instance.clothe,
                    rental_date=date,
                    qty = total_rental_qty,
                    available_qty = avai_qty)
            instance.save()    
                    
                    