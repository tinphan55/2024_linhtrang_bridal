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





# def get_combo_choices():
#         combo_choices = [(c.id, c.name) for c in ComboPhoto.objects.all()]
#         combo_choices.insert(0, ("0", "None"))
#         return combo_choices


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)
    wedding_date= models.DateField(null=False, blank= False)
    # combo = models.IntegerField(choices=get_combo_choices(), default="0", blank=True, null=True)
    note = models.TextField(max_length=500, null= True, blank=True)
    incurred = models.IntegerField(null= True, blank=True, default=0)
    total_price = models.FloatField(default=0)
    total_bill = models.FloatField(default=0)
    paid = models.IntegerField(null= False, blank=False, default=0)
    receivable = models.FloatField(default=0)
    

    def __str__(self):
        return str(self.id) + '_' + str(self.client) 
    
    def return_id_cart(self):
        return self.id

        
    # def save(self, *args, **kwargs):
    #     clothe = ClotheService.objects.filter(cart_id =self.id )
    #     total = clothe.aggregate(total=Sum('total_items'))
    #     total_price = total['total']
    #     if total_price == None:
    #         total_clothe = 0
    #     else:
    #         total_clothe = total_price
        
    #     items_photo = Cart.objects.annotate(total= Sum(F('photoservice__total_items'))).filter(pk=self.pk).values()
    #     if items_photo.count() ==0:
    #         total_photo = 0
    #     else:
    #         total_photo= items_photo[0]['total'] or 0
        
        
    #     items_makeup = Cart.objects.annotate(total= Sum(F('makeupservice__total_items'))).filter(pk=self.pk).values()
    #     if items_makeup.count() ==0:
    #         total_makecup = 0
    #     else:
    #         total_makecup = items_makeup[0]['total'] or 0
        
    #     items_accessory = Cart.objects.annotate(total= Sum(F('accessorysserive__total_items'))).filter(pk=self.pk).values()
    #     if items_accessory.count()==0:
    #         total_accessory = 0
    #     else:
    #         total_accessory = items_accessory[0]['total'] or 0
    #     total =  total_clothe + total_photo + total_makecup + total_accessory
    #     self.total_price = total 

    #     items_incurred = Cart.objects.annotate(total= Sum(F('incurredcart__amount'))).filter(id=self.id).values()
    #     if items_incurred.count() ==0:
    #         self.incurred = 0
    #     else:
    #         self.incurred = items_incurred[0]['total'] or 0
    #     self.total_bill = self.total_price + self.incurred

    #     items_payment = Cart.objects.annotate(total= Sum(F('paymentschedulecart__amount'))).filter(id=self.id).values()
    #     if items_payment.count() ==0:
    #         self.paid = 0
    #     else:
    #         self.paid = items_payment[0]['total'] or 0
    #     self.receivable = self.total_bill - self.paid
        
    #     super(Cart, self).save(*args, **kwargs)

class CartItems(models.Model):
    class Meta:
        abstract = True
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(default=datetime.now)
    price = models.FloatField(blank=True, default=0)
    qty = models.IntegerField(default=1)
    discount = models.IntegerField(null= True, blank=True, default=0)
    is_discount = models.BooleanField(default=False)  
    total_items = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        total_items = self.price*self.qty
        if total_items == None:
            self.total_items = 0
        else:
            self.total_items = total_items
        super(CartItems, self).save(*args, **kwargs)
    
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
        total_items = self.total_items - self.discount
        return '{:,.0f}'.format( total_items)


    
class ClotheService(CartItems):
    clothe = models.ForeignKey(Clothe, on_delete = models.CASCADE,
     limit_choices_to={'is_available': True})
    delivery_date = models.DateField(null= True, blank=True)
    return_date = models.DateField(null= True, blank=True)
    is_returned = models.BooleanField(default=False) 
    returned_at = models.DateTimeField(null=True, blank=True)  
    note = models.TextField(max_length=500, null = True, blank=True)
    noti = models.CharField (max_length=200)
    
    def __str__(self):
        return str(self.clothe)
    
    def save(self, *args, **kwargs):
        self.price = self.clothe.price
        if self.is_discount == True:
            self.discount = self.clothe.ranking.discount * self.qty
        else:
            self.discount = 0
        if self.delivery_date == None:
            self.delivery_date = self.cart.wedding_date - timedelta(days=2)
        if self.return_date == None:
            self.return_date = self.cart.wedding_date + timedelta(days=2) 
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
    

class PhotoService(CartItems):
    package = models.ForeignKey(Photo, on_delete = models.CASCADE, 
        limit_choices_to={'is_available': True})
    note = models.TextField(max_length=500, null= True, blank=True)
    def __str__(self):
        return str(self.package)

    def save(self, *args, **kwargs):
        self.price = self.package.price
        if self.is_discount == True:
            self.discount = self.package.discount* self.qty
        else:
            self.discount = 0
        super(PhotoService, self).save(*args, **kwargs)

    
class MakeupService(CartItems):
    package = models.ForeignKey(Makeup, on_delete = models.CASCADE, 
        limit_choices_to={'is_available': True})
    note = models.TextField(max_length=500, null= True, blank=True)

    def save(self, *args, **kwargs):
        self.price = self.package.price
        if self.is_discount == True:
             self.discount = self.package.discount* self.qty
        else:
            self.discount = 0
        super(MakeupService, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.package)

class AccessorysSerive (CartItems):
    product = models.ForeignKey(Accessory, on_delete = models.CASCADE, 
        limit_choices_to={'is_available': True})
    delivery_date = models.DateField(null= True, blank=True)
    return_date = models.DateField(null= True, blank=True)
    is_returned = models.BooleanField(default=False) 
    returned_at = models.DateTimeField(null=True, blank=True)  
    note = models.TextField(max_length=500, null = True, blank=True)
    noti = models.CharField (max_length=200, null = True, blank=True)
    def __str__(self):
        return str(self.product)
    
    def save(self, *args, **kwargs):
        self.price = self.product.price
        if self.is_discount == True:
             self.discount = self.product.discount * self.qty
        else:
            self.discount = 0
        if self.delivery_date == None:
            self.delivery_date = self.cart.wedding_date - timedelta(days=2)
        if self.return_date == None:
            self.return_date = self.cart.wedding_date + timedelta(days=2) 
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
    
class IncurredCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  
    description = models.TextField(max_length=500, null=False)
    created_at = models.DateTimeField(default=datetime.now)
    amount =  models.IntegerField(null= False, default=0)
    def __str__(self):
        return str(self.cart)
    
class PaymentScheduleCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  
    amount =  models.IntegerField(null= False, default=0)
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=datetime.now)
   
    def __str__(self):
        return str(self.cart)
    

class ReturnClothe(ClotheService):
    class Meta:
        proxy = True

    def __str__(self):
        return str(self.clothe.code)
    
    
        

class ReturnAccessory (AccessorysSerive):
    class Meta:
        proxy = True
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