from order.models import *
from itertools import chain
from bills.models import *

def total_cart_raw(pk):
    clothe_items = ClotheService.objects.filter(cart_id = pk ).values()
    photo_items = PhotoService.objects.filter(cart_id = pk ). values()
    makeup_items = MakeupService.objects.filter(cart_id = pk ). values()
    accessory_items= AccessorysSerive.objects.filter(cart_id = pk ). values()
    cart = list(chain(clothe_items, photo_items,makeup_items,accessory_items  ))
    total_price = 0
    for items in cart:
        total_price = total_price + items['total_items']
    return total_price


def total_discount_raw(pk):
    clothe_items = ClotheService.objects.filter(cart_id = pk ).values()
    photo_items = PhotoService.objects.filter(cart_id = pk ). values()
    makeup_items = MakeupService.objects.filter(cart_id = pk ). values()
    accessory_items= AccessorysSerive.objects.filter(cart_id = pk ). values()
    cart = list(chain(clothe_items, photo_items,makeup_items,accessory_items  ))
    total_discount = 0
    for items in cart:
        if items['discount'] == None:
                items['discount'] = 0
                total_discount = total_discount + items['discount']
        else:
                total_discount = total_discount + items['discount']
    return total_discount

def total_incurred_raw(pk):
    incurred_items = IncurredCart.objects.filter(cart_id = pk ).values()
    total = 0
    for items in incurred_items:
        total = total + items['amount']
    return total 

def total_payment_raw(pk):
    payment_items = PaymentScheduleCart.objects.filter(cart_id = pk ).values()
    total = 0
    for items in payment_items:
        total = total + items['amount']
    return total 

def total_row(pk):
    total = total_cart_raw(pk) + total_incurred_raw(pk) - total_discount_raw(pk)
    return total

def get_total_values_bill(pk):
    bill_values ={}
    cart_list = Cart.objects.filter(billitems__bill_id=pk)
    total_retail  = 0
    discount = 0
    incurred = 0
    paid = 0
    for qs in cart_list:
        total_retail  = total_cart_raw(qs.pk) +total_retail 
        discount = total_discount_raw(qs.pk) + discount
        incurred = total_incurred_raw(qs.pk) + incurred
        total = total_retail +incurred-discount
        paid = total_payment_raw(qs.pk)+ paid
        receivable = total - paid
    bill_values['total_retail'] =total_retail
    bill_values['discount'] = discount
    bill_values['incurred'] = incurred
    bill_values['total'] =  total
    bill_values['paid'] = paid
    bill_values['receivable'] = receivable
    return bill_values
       
def lookup_items_bill(pk):
    bill = Bill.objects.get(pk=pk)
    bill_items = bill.billitems_set.all()
    clothe_service = []
    photo_service = []
    makup_service = []
    accessory_service =[]
    for item in bill_items:
        clothe_service.append(item.cart.clotheservice_set.all())
        clothe_service.append(item.cart.accessorysserive_set.all())
        clothe_service=[qset for qset in clothe_service if qset and len(qset) > 0]
        photo_service.append(item.cart.photoservice_set.all())
        photo_service=[qset for qset in photo_service if qset and len(qset) > 0]
        makup_service.append(item.cart.makeupservice_set.all())
        makup_service=[qset for qset in makup_service if qset and len(qset) > 0]
    service_items = {
            'clothe_bill':clothe_service,
            'photo_bill':photo_service,
            'makup_bill': makup_service}
    return service_items
