from django.contrib import admin
from .models import *
from django.urls import reverse
from django.utils.html import format_html
from django.utils.html import format_html_join


# Register your models here.

class BillItemsInline(admin.TabularInline):
    model = BillItems
    fields =('cart',)
    

class BillAdmin(admin.ModelAdmin):
    inlines = [BillItemsInline]
    list_display = ('code_bill','created_date','cart_with_links','client_full_name','client_phone','title_with_link')
    fields = ('note',"next_payment")
    list_display_links = ('code_bill',)
    search_fields = ('id',)
    list_filter = ('created_date',)

    
    def code_bill (self,obj):
            month = datetime.now().month
            return  str(obj.id) +"_"+ str(month) 
    code_bill.short_description = 'Mã'

           

    def client_full_name(self, obj):
        first_item = obj.billitems_set.first()
        if first_item is None:
            return "None" 
        else:
            return first_item.cart.client.full_name
    client_full_name.short_description = 'Tên KH'
 

    def client_phone(self, obj):
        first_item = obj.billitems_set.first()
        if first_item is None:
            return "None" 
        else:
            return obj.billitems_set.first().cart.client.phone
    client_phone.short_description = 'Điện thoại KH'

    
    def title_with_link(self, obj):
        first_item = obj.billitems_set.first()
        if first_item is None:
            return "None" 
        else:
            url = reverse('bills:details', args=[obj.pk])
            return format_html("<a href='{}' target='_blank' style='background-color: #007bff; border-radius: 5px; color: white; padding: 5px;'>Click xem bill</a>", url)
    title_with_link.short_description = 'Xem hóa đơn'


    def cart_with_links(self, obj):
        first_item = obj.billitems_set.first()
        if first_item is None:
            return "None" 
        else:
            cart_list = []
            for item in obj.billitems_set.all():
                url = reverse('admin:order_cart_change', args=[item.cart.id])
                cart_list.append(format_html("<a href='{}' target='_blank'>{}</a><br>", url, item.cart))
            return format_html(''.join(cart_list))

    
    cart_with_links.short_description = 'Cart'

    # def pdf(self, obj):
    #     first_item = obj.billitems_set.first()
    #     if first_item is None:
    #         return "None" 
    #     else:
    #         url = reverse('bills:pdf', args=[obj.pk])
    #         return format_html("<a href='{}' target='_blank' style='background-color: #007bff; border-radius: 5px; color: white; padding: 5px;'>Tải pdf</a>", url)
    



   

  

admin.site.register(Bill, BillAdmin)




