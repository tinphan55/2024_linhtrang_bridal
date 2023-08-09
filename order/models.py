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
from django.db.models.signals import post_save, post_delete
from telegram import Bot
from infobot import *
from django.dispatch import receiver





class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True, blank= True, 
                             verbose_name="Người tạo")
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
    receivable = models.FloatField(default=0)
    

    def __str__(self):
        return str(self.id) + '_' + str(self.client) 
    
    def return_id_cart(self):
        return self.id
    

    @property
    def latest_paid(self):
        latest_payment = PaymentScheduleCart.objects.filter(cart=self).aggregate(Max('created_at'))
        return latest_payment['created_at__max']
    
    @property
    def total_clothe(self):
        clothe= ClotheService.objects.filter(cart_id = self.pk )
        total = sum(i.total_items for i in clothe)
        return total
   
    
    @property
    def total_photo(self):
        photo= PhotoService.objects.filter(cart_id = self.pk )
        total = sum(i.total_items for i in photo)
        return total
    @property
    def total_makup(self):
        makup= MakeupService.objects.filter(cart_id = self.pk )
        total = sum(i.total_items for i in makup)
        return total
    
    #DT phụ kiện sẽ tính có chọn lọc, dưa vào field is_hr để sum
    @property
    def total_accessory_hr(self):
        accessory= AccessorysSerive.objects.filter(cart_id = self.pk, product__is_hr = True)
        total = sum(i.total_items for i in accessory)
        return total
    
    @property
    def total_accessory(self):
        accessory= AccessorysSerive.objects.filter(cart_id = self.pk)
        total = sum(i.total_items for i in accessory)
        return total
    
    @property
    def str_total_clothe(self):
        return '{:,.0f}'.format(self.total_clothe)
    @property
    def str_total_photo(self):
        return '{:,.0f}'.format(self.total_photo)
    @property
    def str_total_makup(self):
        return '{:,.0f}'.format(self.total_makup)
    @property
    def str_total_accessory(self):
        return '{:,.0f}'.format(self.total_accessory)
    
    @property
    def total_discount_raw(self):
        clothe_items = ClotheService.objects.filter(cart_id = self.pk ).values()
        photo_items = PhotoService.objects.filter(cart_id = self.pk ). values()
        makeup_items = MakeupService.objects.filter(cart_id = self.pk ). values()
        accessory_items= AccessorysSerive.objects.filter(cart_id = self.pk ). values()
        cart = list(chain(clothe_items, photo_items,makeup_items,accessory_items  ))
        total_discount = 0
        for items in cart:
            if items['discount'] == None:
                    items['discount'] = 0
                    total_discount = total_discount + items['discount']
            else:
                    total_discount = total_discount + items['discount']
        return total_discount
    #doanh thu trước giảm giá
    @property
    def total_cart_raw(self):
        return self.total_clothe + self.total_photo + self.total_makup +self.total_accessory +self.total_discount_raw
    
    @property
    def total_incurred_raw(self):
        incurred_items = IncurredCart.objects.filter(cart_id = self.pk ).values()
        total = 0
        for items in incurred_items:
            total = total + items['amount']
        return total 
    
    @property
    def total_payment_raw(self):
        payment_items = PaymentScheduleCart.objects.filter(cart_id = self.pk ).values()
        total = 0
        for items in payment_items:
            total = total + items['amount']
        return total 
     #doanh thu sau giảm giá
    @property
    def total_raw(self):
        total = self.total_cart_raw + self.total_incurred_raw - self.total_discount_raw
        return total
    @property
    def str_total_raw(self):
        return '{:,.0f}'.format(self.total_raw)
    @property
    def receivable_raw(self):
        total = self.total_raw - self.total_payment_raw
        return total
    
    @property
    def total_deposit_raw(self):
        clothe_items = ClotheService.objects.filter(cart_id = self.pk )
        clothe =sum(i.total_deposit for i in clothe_items )
        photo_items = PhotoService.objects.filter(cart_id = self.pk )
        photo =sum(i.total_deposit for i in photo_items )
        makeup_items = MakeupService.objects.filter(cart_id = self.pk )
        makup = sum(i.total_deposit for i in makeup_items )
        accessory_items= AccessorysSerive.objects.filter(cart_id = self.pk )
        acces = sum(i.total_deposit for i in accessory_items)
        return clothe + photo +acces + makup
        

    
    

class CartItems(models.Model):
    class Meta:
        abstract = True
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(default=datetime.now)
    price = models.FloatField(blank=True, default=0, verbose_name="Giá")
    qty = models.IntegerField(default=1, verbose_name="Số lượng")
    discount = models.IntegerField(null= True, blank=True, default=0,verbose_name= "Giảm giá")
    is_discount = models.BooleanField(default=False, verbose_name="Có giảm giá")  
    # total_items = models.IntegerField(default=0, verbose_name="Tổng tiền")
    # str_total_items = models.CharField(max_length=50,null= True, blank=True, verbose_name="Tổng tiền")
    # str_price = models.CharField(max_length=50,null= True, blank=True, verbose_name="Giá")
    # str_discount = models.CharField(max_length=50,null= True, blank=True, verbose_name="Giảm giá")
    

    @property
    def total_items(self):
        total = self.price*self.qty
        if total == None:
            total = 0
        else:
            if self.discount ==None:
                total = total
            else:
                total = total - self.discount
        return total
    
    
    
    @property
    def str_price(self):
        price = self.price
        return '{:,.0f}'.format(price)
    @property
    def str_discount(self):
        discount = self.discount
        return '{:,.0f}'.format( discount)
    
    @property
    def str_total_items(self):
        return '{:,.0f}'.format( self.total_items)


    
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
    # total_deposit  = models.CharField(max_length=50,null= True, blank=True, verbose_name="Tổng đặt cọc")


    class Meta:
        verbose_name = 'Cho thuê đồ cưới'
        verbose_name_plural = 'Cho thuê đồ cưới'
    
    def __str__(self):
        return str(self.clothe)
    
    def save(self, *args, **kwargs):
        self.price = self.clothe.price
        # Đặt giá trị vô cùng lớn và vô cùng nhỏ cho NoneType
        INFINITY_DATE = date.max
        MINUS_INFINITY_DATE = date.min
        max_wedding_date = max(self.cart.wedding_date or MINUS_INFINITY_DATE,self.cart.wedding_date_2 or MINUS_INFINITY_DATE)
        min_wedding_date = min(self.cart.wedding_date or INFINITY_DATE, self.cart.wedding_date_2 or INFINITY_DATE)
        # max_date = max(wedding_date or MINUS_INFINITY_DATE, wedding_date2 or MINUS_INFINITY_DATE)
        if self.is_discount == True:
            self.discount = self.clothe.ranking.discount * self.qty
        else:
            self.discount = 0
        if self.delivery_date == None:
            self.delivery_date = min_wedding_date - timedelta(days=2)
        if self.return_date == None:
            self.return_date = max_wedding_date + timedelta(days=2) 
        super(ClotheService, self).save(*args, **kwargs)
    
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
    
    @property
    def total_deposit(self):
        deposit = self.clothe.deposit
        return deposit*self.qty
    
# @receiver(post_save, sender=ClotheService)
# def save_clothe_service(sender, instance, created, **kwargs):

              


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
        if self.is_discount == True:
            self.discount = self.package.discount* self.qty
        else:
            self.discount = 0
        super(PhotoService, self).save(*args, **kwargs)
    @property
    def total_deposit(self):
        deposit = self.package.deposit
        return deposit*self.qty

    
class MakeupService(CartItems):
    package = models.ForeignKey(Makeup, on_delete = models.CASCADE, 
        limit_choices_to={'is_available': True}, verbose_name='Gói trang điểm')
    note = models.TextField(max_length=500, null= True, blank=True, verbose_name="Ghi chú")
    class Meta:
        verbose_name = 'Trang điểm'
        verbose_name_plural = 'Trang điểm'
    def save(self, *args, **kwargs):
        self.price = self.package.price
        if self.is_discount == True:
             self.discount = self.package.discount* self.qty
        else:
            self.discount = 0
        super(MakeupService, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.package)
    @property
    def total_deposit(self):
        deposit = self.package.deposit
        return deposit*self.qty

class AccessorysSerive (CartItems):
    product = models.ForeignKey(Accessory, on_delete = models.CASCADE, 
        limit_choices_to={'is_available': True}, verbose_name='Sản phẩm')
    delivery_date = models.DateField(null= True, blank=True, verbose_name='Ngày giao')
    return_date = models.DateField(null= True, blank=True,verbose_name= "Ngày hẹn trả")
    is_returned = models.BooleanField(default=False, verbose_name="Đã trả") 
    returned_at = models.DateTimeField(null=True, blank=True, verbose_name="Ngày trả")  
    note = models.TextField(max_length=500, null = True, blank=True, verbose_name="Ghi chú")
    noti = models.CharField (max_length=200, null = True, blank=True)
    def __str__(self):
        return str(self.product)
    class Meta:
        verbose_name = 'Phụ kiện'
        verbose_name_plural = 'Phụ kiện'
    
    def save(self, *args, **kwargs):
        self.price = self.product.price
        INFINITY_DATE = date.max
        MINUS_INFINITY_DATE = date.min
        max_wedding_date = max(self.cart.wedding_date or MINUS_INFINITY_DATE,self.cart.wedding_date_2 or MINUS_INFINITY_DATE)
        min_wedding_date = min(self.cart.wedding_date or INFINITY_DATE, self.cart.wedding_date_2 or INFINITY_DATE)
        if self.is_discount == True:
             self.discount = self.product.discount * self.qty
        else:
            self.discount = 0
        if self.delivery_date == None:
            self.delivery_date = min_wedding_date - timedelta(days=2)
        if self.return_date == None:
            self.return_date = max_wedding_date + timedelta(days=2) 
        today = date.today()
        super(AccessorysSerive, self).save(*args, **kwargs)
    
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
    @property
    def total_deposit(self):
        deposit = self.product.deposit
        return deposit*self.qty
    
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

# class CartCombo (models.Model):
#     name = models.CharField(max_length=100)
#     clothe = models.ManyToManyField(Clothe)
#     def save_model(self, request, form):
#         if form.is_valid():
#             self.name.save()
#             self.clothe.save_m2m()

# Gửi tin nhắn telegram

@receiver(post_save, sender=Cart)
def update_manage_clothe(sender, instance, created, **kwargs):
        INFINITY_DATE = date.max
        MINUS_INFINITY_DATE = date.min
        max_wedding_date = max(instance.wedding_date or MINUS_INFINITY_DATE,instance.wedding_date_2 or MINUS_INFINITY_DATE)
        min_wedding_date = min(instance.wedding_date or INFINITY_DATE, instance.wedding_date_2 or INFINITY_DATE)
        clothe = ClotheService.objects.filter(cart = instance.pk)
        accessory = AccessorysSerive.objects.filter(cart = instance.pk)
        for item in clothe:
            item.delivery_date = min_wedding_date - timedelta(days=2)
            item.return_date = max_wedding_date + timedelta(days=2)
            item.save()
        for item in accessory:
            item.delivery_date = min_wedding_date - timedelta(days=2)
            item.return_date = max_wedding_date + timedelta(days=2)
            item.save()


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