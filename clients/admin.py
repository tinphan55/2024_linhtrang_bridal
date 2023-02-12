from django.contrib import admin
from .models import *
from order.models import Cart
from order.admin import total_row


def total_client_cart(obj):
    client_items = Cart.objects.filter(client_id = obj.id )
    total = 0
    for items in client_items:
        total = total + total_row(items)
    return total 

class ClientAdmin (admin.ModelAdmin):
    model = Client
    list_display=('full_name', 'code', 'phone','total_cart_')
    field =['full_name', 'code', 'phone','address','birthday','total_cart_']
    search_fields = ('full_name', 'code', 'phone')
    readonly_fields= ['total_cart_']

    @admin.display(description='total_cart_')
    def total_cart_(self, obj):
        total = total_client_cart(obj)
        return f"{total:,}"

admin.site.register(Client, ClientAdmin)
