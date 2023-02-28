from order.models import *
from itertools import chain
from bills.models import *
from django.template import loader
from members.models import *
from event_calendar.models import *
from unittest import result
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import logging
import os
from reportlab.lib.pagesizes import letter


logger = logging.getLogger(__name__)

def html2pdf(template_source, context_dict={}):
    template = get_template(template_source)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, pagesize=letter)
    if not pdf.err:
        return result.getvalue()
    else:
        logger.error(pdf.err)
        return None
        
def fetch_resources(uri, rel):
    """
    Callback to allow xhtml2pdf to fetch additional resources such as
    stylesheets and images.
    """
    if uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ''))
    else:
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))
    return path

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

def context_bill(pk):
    bills = Bill.objects.get(pk=pk)
    items = lookup_items_bill(pk)
    cart= bills.billitems_set.first().cart
    list_cart = bills.billitems_set.all()
    staff = Member.objects.get(id_member_id=cart.user.id)
    clothe = items['clothe_bill']
    photo = items['photo_bill']
    makup = items['makup_bill']
    code = str(pk)+ "_" + str(datetime.now().month)
    event = []
    for item in  list_cart:
        event_item = item.cart.event_set.all()
        event.append(event_item)
    
    date_photo = None
    date_makup = None

    for item in event:
        date_photo = item.filter(title ='photo')
        if date_photo.exists():
            date_photo = date_photo[0]
            break
    
    for item in event:
        date_makup = item.filter(title ='makeup')
        if date_makup.exists():
            date_makup = date_makup[0]
            break
       
    if len(clothe) ==0:
        first_clothe =""
    else:
        first_clothe = clothe[0][0]
        
    bill_total = get_total_values_bill(pk)
    total_retail = f"{bill_total['total_retail']:,}"
    discount = f"{bill_total['discount']:,}"
    incurred = f"{bill_total['incurred']:,}"
    total = f"{bill_total['total']:,}"
    paid = f"{bill_total['paid']:,}"
    receivable_raw = bill_total['receivable']
    incurred_raw = bill_total['incurred']
    receivable = f"{bill_total['receivable']:,}"
    context = {
        'bills':bills,
        'code': code,
        'items':items,
        'staff':staff,
        'clothe': clothe,
        'cart': cart ,
        'first_clothe': first_clothe,
        'total_retail': total_retail,
        'discount': discount,
        'incurred': incurred,
        'total': total,
        'paid' : paid,
        'receivable': receivable,
        'date_photo': date_photo,
        "date_makup":date_makup,
        'receivable_raw':receivable_raw,
        'incurred_raw': incurred_raw
    }
    return context