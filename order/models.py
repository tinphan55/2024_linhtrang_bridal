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




class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)
    wedding_date= models.DateField(null=False, blank= False)
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
    
    def my_view(self,request, *args, **kwargs):
        username = None
        if request.user.is_authenticated():
            self.user = request.user.username
        super(Cart,self).save(*args, **kwargs)
    

        
    def save(self, *args, **kwargs):
        clothe = ClotheService.objects.filter(cart_id =self.id )
        total = clothe.aggregate(total=Sum('total_items'))
        total_price = total['total']
        if total_price == None:
            total_clothe = 0
        else:
            total_clothe = total_price
        
        items_photo = Cart.objects.annotate(total= Sum(F('photoservice__total_items'))).filter(pk=self.pk).values()
        if items_photo.count() ==0:
            total_photo = 0
        else:
            total_photo= items_photo[0]['total'] or 0
        
        
        items_makeup = Cart.objects.annotate(total= Sum(F('makeupservice__total_items'))).filter(pk=self.pk).values()
        if items_makeup.count() ==0:
            total_makecup = 0
        else:
            total_makecup = items_makeup[0]['total'] or 0
        
        items_accessory = Cart.objects.annotate(total= Sum(F('accessorysserive__total_items'))).filter(pk=self.pk).values()
        if items_accessory.count()==0:
            total_accessory = 0
        else:
            total_accessory = items_accessory[0]['total'] or 0
        total =  total_clothe + total_photo + total_makecup + total_accessory
        self.total_price = total 

        items_incurred = Cart.objects.annotate(total= Sum(F('incurredcart__amount'))).filter(id=self.id).values()
        if items_incurred.count() ==0:
            self.incurred = 0
        else:
            self.incurred = items_incurred[0]['total'] or 0
        self.total_bill = self.total_price + self.incurred

        items_payment = Cart.objects.annotate(total= Sum(F('paymentschedulecart__amount'))).filter(id=self.id).values()
        if items_payment.count() ==0:
            self.paid = 0
        else:
            self.paid = items_payment[0]['total'] or 0
        self.receivable = self.total_bill - self.paid
        
        super(Cart, self).save(*args, **kwargs)

class CartItems(models.Model):
    class Meta:
        abstract = True
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)    
    price = models.FloatField(blank=True, default=0)
    qty = models.IntegerField(default=1)
    total_items = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        total_items = self.price*self.qty
        if total_items == None:
            self.total_items = 0
        else:
            self.total_items = total_items
        super(CartItems, self).save(*args, **kwargs)
    
class ClotheService(CartItems):
    clothe = models.ForeignKey(Clothe, on_delete = models.CASCADE,
     limit_choices_to={'is_available': True})
    delivery_date = models.DateField()
    return_date = models.DateField()
    is_returned = models.BooleanField(default=True) 
    returned_at = models.DateTimeField(null=True, blank=True)  
    note = models.TextField(max_length=500, null = True, blank=True)
    noti = models.CharField (max_length=200)
    def __str__(self):
        return str(self.clothe)
    
    def save(self, *args, **kwargs):
        self.price = Clothe.objects.get(id=self.clothe_id).price
        self.delivery_date = self.cart.wedding_date - timedelta(days=2)
        self.return_date = self.cart.wedding_date + timedelta(days=2) 
        today = date.today()
        if today > self.delivery_date and self.returned_at == None:
            self.is_returned = False
        if self.is_returned == False and today > self.return_date:
            self.noti = str('Thu hoi do cuoi, da tre hen. Ngay thu hoi theo hen la') + str(self.return_date)
        super(ClotheService, self).save(*args, **kwargs)

class PhotoService(CartItems):
    package = models.ForeignKey(Photo, on_delete = models.CASCADE, 
        limit_choices_to={'is_available': True})
    note = models.TextField(max_length=500, null= True, blank=True)
    def __str__(self):
        return str(self.package)

    def save(self, *args, **kwargs):
        self.price = Photo.objects.get(id=self.package_id).price
        super(PhotoService, self).save(*args, **kwargs)

    
class MakeupService(CartItems):
    package = models.ForeignKey(Makeup, on_delete = models.CASCADE, 
        limit_choices_to={'is_available': True})
    note = models.TextField(max_length=500, null= True, blank=True)
    def save(self, *args, **kwargs):
        self.price = Makeup.objects.get(id=self.package_id).price
        super(MakeupService, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.package)

class AccessorysSerive (CartItems):
    product = models.ForeignKey(Accessory, on_delete = models.CASCADE, 
        limit_choices_to={'is_available': True})
    def __str__(self):
        return str(self.product)
    
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
    

class ReturnItems (ClotheService):
    class Meta:
        proxy = True
    


    def __str__(self):
        return str(self.clothe.name)


    