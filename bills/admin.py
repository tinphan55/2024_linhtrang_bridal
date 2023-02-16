from django.contrib import admin
from .models import *
from django.urls import reverse
from django.utils.html import format_html


# Register your models here.

class BillItemsInline(admin.TabularInline):
    model = BillItems
    fields =('cart',)
    

class BillAdmin(admin.ModelAdmin):
    inlines = [BillItemsInline]
    list_display = ('id','created_date','client_full_name','client_phone','title_with_link')
    fields = ('note',)
    list_display_links = ('id',)
    search_fields = ('client_phone',)
    list_filter = ('created_date',)

    def title_with_link(self, obj):
        first_item = obj.billitems_set.first()
        if first_item is None:
            return "None" 
        else:
            url = reverse('bills:details', args=[obj.pk])
            return format_html("<a href='{}' target='_blank'>{}</a>", url, obj.code)
    title_with_link.short_description = 'Link_Bill'
  


    def client_full_name(self, obj):
        first_item = obj.billitems_set.first()
        if first_item is None:
            return "None" 
        else:
            return first_item.cart.client.full_name
    
    def client_phone(self, obj):
        first_item = obj.billitems_set.first()
        if first_item is None:
            return "None" 
        else:
            return obj.billitems_set.first().cart.client.phone

    client_full_name.short_description = 'Client'
    client_phone.short_description = 'Phone'
    

admin.site.register(Bill, BillAdmin)




