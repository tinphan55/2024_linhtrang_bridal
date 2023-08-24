from django.contrib import admin
from .models import *
from order.models import *







class ClientAdmin (admin.ModelAdmin):
    model = Client
    list_display=('full_name', 'code', 'phone','address','str_total_values')
    field =['full_name', 'code', 'phone','ward','birthday','note','str_total_values']
    search_fields = ('full_name', 'code', 'phone')
    readonly_fields= ['address','str_total_values']


admin.site.register(Client, ClientAdmin)

@receiver([post_save, post_delete], sender=Cart)
def total_client_cart_row(sender, instance, **kwargs):
    items = Client.objects.get(pk =  instance.client.pk)
    cart = Cart.objects.filter(client_id = instance.client.pk)
    items.total_values =sum(i.total_raw  for i in cart)
    items.str_total_values = '{:,.0f}'.format(items.total_values)
    items.save()


  

