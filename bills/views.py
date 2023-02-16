from django.shortcuts import render
from django.http import HttpResponse
from bills.function import *
from itertools import chain
from django.template import loader
from members.models import *

def billdetail(request, pk):
    bills = Bill.objects.get(pk=pk)
    items = lookup_items_bill(pk)
    cart= bills.billitems_set.first().cart
    staff = Member.objects.get(id_member_id=cart.user.id)
    date_photo = cart.event_set.filter(title = 'photo')
    date_makup = cart.event_set.filter(title = 'makeup')
    if len(date_photo) == 0:
        date_photo =""
    else:
        date_photo= date_photo[0]

    if len(date_makup) == 0:
        date_makup =""
    else:
        date_makup = date_makup[0]


    clothe = items['clothe_bill']
    photo = items['photo_bill']
    makup = items['makup_bill']
    first_clothe = clothe[0][0]
    bill_total = get_total_values_bill(pk)
    total_retail = f"{bill_total['total_retail']:,}"
    discount = f"{bill_total['discount']:,}"
    incurred = f"{bill_total['incurred']:,}"
    total = f"{bill_total['total']:,}"
    paid = f"{bill_total['paid']:,}"
    receivable = f"{bill_total['receivable']:,}"
    template = loader.get_template('bills/details.html')
    context = {
        'bills':bills,
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
    }
    return HttpResponse(template.render(context, request))


