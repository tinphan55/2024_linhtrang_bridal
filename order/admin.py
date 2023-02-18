from django.utils.html import format_html
from services_admin import *
from django.contrib import admin
from .models import *
from django.db.models import  Sum
from event_calendar.models import Event
from datetime import datetime, timedelta, date
from itertools import chain
from .forms import *

def convent_str_total_items(obj):
    total_items = obj.total_items
    return f"{total_items:,}"

class ClotheServiceInline(admin.StackedInline):
    form = ClotheServiceForm
    model= ClotheService
    fields = ['clothe','qty','discount','delivery_date','return_date','total_items_']
    readonly_fields = ['total_items_',]
    @admin.display(description='total_items_')
    def total_items_(self,obj):
        return convent_str_total_items(obj, )
    
@admin.action(description='Confirm Clothe is returned')
def returned (modeladmin, request, queryset):
    for ReturnItems in queryset:
        if ReturnItems.is_returned == False:
            queryset.update(is_returned = True )
            queryset.update(returned_at = datetime.now())
    

@admin.action(description='NOT returned')   
def not_return (modeladmin, request, queryset):
    queryset.update(is_returned = False )

class ReturnItemsAdmin(admin.ModelAdmin):
    def clothe_id(self, obj):
        return obj.clothe.id
    model = ReturnItems
    list_display = ('cart','clothe','get_color','qty' ,'delivery_date', 'return_date', 'is_returned', 'returned_at' )
    fields = ['clothe','noti','qty', 'delivery_date', 'return_date', 'is_returned', 'note', 'returned_at' ]
    readonly_fields = ['clothe','qty', 'delivery_date', 'return_date','returned_at', 'noti']
    list_display_links = ('clothe',)
    list_filter =  ('is_returned','returned_at','cart__wedding_date' )
    search_fields = ('clothe__code','clothe__name', 'cart__client__phone', 'cart__id')
    #search_help_text = ('test')
    actions = [returned, not_return]
    admin.site.disable_action('delete_selected')
    @admin.display(description='color_')
    def get_color(self, obj):
        return obj.clothe.color
    
    



class PhotoScheduleInline(admin.StackedInline):
    model =  Event 
    extra = 1
    fields = ['title','start_time','end_time','description']
   

class MakeupServiceInline(admin.StackedInline):
    model =  MakeupService
    fields = ['package','note','discount','total_items_']
    #raw_id_fields = ['product']
    readonly_fields = ['total_items_',]
    extra = 1
    @admin.display(description='total_items_')
    def total_items_(self,obj):
        return convent_str_total_items(obj, )

class AccessoryServiceInline(admin.TabularInline):
    model =  AccessorysSerive
    fields = ['product','qty','discount','total_items_']
    #raw_id_fields = ['product']
    readonly_fields = ['total_items_',]
    @admin.display(description='total_items_')
    def total_items_(self,obj):
        return convent_str_total_items(obj, )
    

class PhotoServiceInline(admin.StackedInline):
    model = PhotoService 
    fields = ['package','discount','note','total_items_']
    readonly_fields = ['total_items_', ]
    extra = 1
    @admin.display(description='total_items_')
    def total_items_(self,obj):
        return convent_str_total_items(obj, )

class IncurredCartInline(admin.StackedInline):
    form = IncurredCartForm
    model = IncurredCart 
    extra = 1 
    fields = ['amount','description','created_at']

class PaymentCartInline(admin.StackedInline):
    model = PaymentScheduleCart
    extra = 3 
    fields = ['amount','description','created_at']
   
        

#Cong thuc tinh tong bill
def total_cart_raw(obj):
    clothe_items = ClotheService.objects.filter(cart_id = obj.id ).values()
    photo_items = PhotoService.objects.filter(cart_id = obj.id ). values()
    makeup_items = MakeupService.objects.filter(cart_id = obj.id ). values()
    accessory_items= AccessorysSerive.objects.filter(cart_id = obj.id ). values()
    cart = list(chain(clothe_items, photo_items,makeup_items,accessory_items  ))
    total_price = 0
    for items in cart:
        total_price = total_price + items['total_items']
    return total_price

def total_discount_raw(obj):
    clothe_items = ClotheService.objects.filter(cart_id = obj.id ).values()
    photo_items = PhotoService.objects.filter(cart_id = obj.id ). values()
    makeup_items = MakeupService.objects.filter(cart_id = obj.id ). values()
    accessory_items= AccessorysSerive.objects.filter(cart_id = obj.id ). values()
    cart = list(chain(clothe_items, photo_items,makeup_items,accessory_items  ))
    total_discount = 0
    for items in cart:
        if items['discount'] == None:
                items['discount'] = 0
                total_discount = total_discount + items['discount']
        else:
                total_discount = total_discount + items['discount']
    return total_discount

def total_incurred_raw(obj):
    incurred_items = IncurredCart.objects.filter(cart_id = obj.id ).values()
    total = 0
    for items in incurred_items:
        total = total + items['amount']
    return total 

def total_payment_raw(obj):
    payment_items = PaymentScheduleCart.objects.filter(cart_id = obj.id ).values()
    total = 0
    for items in payment_items:
        total = total + items['amount']
    return total 

def total_row(obj):
    total = total_cart_raw(obj) + total_incurred_raw(obj) - total_discount_raw(obj)
    return total




def receivable_row(obj):
    total = total_row(obj) - total_payment_raw(obj)
    return total

class CartAdmin(admin.ModelAdmin):
    model= Cart 
    form = CartForm
    list_display=('id','user','client','created_at', 'total_cart','total_discount', 'total_incurred', 'total', 'paid_','receivable_', 'wedding_date')
    fields = ['user','client','wedding_date','note','total_cart', 'total_discount','total_incurred', 'total','paid_', 'receivable_']
    list_display_links=('client',)
    search_fields=('client__code',)
     #['created_at','wedding_date',]
    readonly_fields = [ 'created_at','total_cart','total_discount', 'total_incurred', 'total', 'paid_','receivable_']
    list_filter = ('created_at','user__username', 'client__full_name')
    inlines = [PaymentCartInline,ClotheServiceInline,PhotoServiceInline, MakeupServiceInline, AccessoryServiceInline,IncurredCartInline,PhotoScheduleInline]
    


    @admin.display(description='total_cart')
    def total_cart(self, obj):
        total_price = total_cart_raw(obj)
        return f"{total_price:,}"

    @admin.display(description='total_incurred')
    def total_incurred(self, obj):
        total = total_incurred_raw(obj)
        return f"{total:,}"
    
    @admin.display(description='total')
    def total(self, obj):
        total = total_row(obj)
        return f"{total:,}"

    @admin.display(description='paid_')
    def paid_(self, obj):
        total = total_payment_raw(obj)
        return f"{total:,}"

    @admin.display(description='receivable_')
    def receivable_(self, obj):
        total = receivable_row(obj)
        return f"{total:,}"

    @admin.display(description='total_discount')
    def total_discount (self, obj):
        total_discount = total_discount_raw(obj)
        return f"{total_discount:,}"
    

   

admin.site.register(Cart,CartAdmin )
admin.site.register(ReturnItems, ReturnItemsAdmin)

