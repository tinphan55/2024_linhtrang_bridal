from django.shortcuts import render
from django.http import HttpResponse
from bills.function import *
from itertools import chain
from django.template import loader
from members.models import *
from event_calendar.models import *

def billdetail(request, pk):
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
    template = loader.get_template('bills/details.html')
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
    return HttpResponse(template.render(context, request))


