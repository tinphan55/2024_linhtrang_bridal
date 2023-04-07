from django.contrib import admin
from .models import *
from order.models import *




def total_client_cart_row(obj):
    client_items = Cart.objects.filter(client_id = obj )
    return sum(i.total_raw for i in client_items)



class ClientAdmin (admin.ModelAdmin):
    model = Client
    list_display=('full_name', 'code', 'phone','total_cart_')
    field =['full_name', 'code', 'phone','address','birthday','total_cart_']
    search_fields = ('full_name', 'code', 'phone')
    readonly_fields= ['total_cart_']

    @admin.display(description='Tổng tiền dùng dịch vụ')
    def total_cart_(self, obj):
        total = total_client_cart_row(obj.id)
        return f"{total:,}"

admin.site.register(Client, ClientAdmin)
