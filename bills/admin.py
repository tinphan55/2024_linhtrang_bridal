from django.contrib import admin
from .models import *
from django.urls import reverse
from django.utils.html import format_html


# Register your models here.

class BillItemsInline(admin.TabularInline):
    model = BillItems
    fields =('cart',)
    

class BillAdmin(admin.ModelAdmin):
    fields = ('code','note')
    list_display = ('id','client_full_name','created_date','client_phone','title_with_link')
    list_display_links = ('client_full_name',)
    search_fields = ('client_phone',)
    list_filter = ('created_date',)
    inlines = [BillItemsInline]
    
    def title_with_link(self, obj):
        url = reverse('bills:typebills', args=[obj.pk])
        return format_html("<a href='{}' target='_blank'>{}</a>", url, obj.code)
    title_with_link.short_description = 'Link_Bill'

    def client_full_name(self, obj):
        return obj.billitems_set.first().cart.client.full_name
    def client_phone(self, obj):
        return obj.billitems_set.first().cart.client.phone

    client_full_name.short_description = 'Client'
    client_phone.short_description = 'Phone'
    

admin.site.register(Bill, BillAdmin)




