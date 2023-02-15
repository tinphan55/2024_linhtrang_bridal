from django.shortcuts import render
from django.http import HttpResponse
from bills.function import *
from itertools import chain
from django.template import loader

def billdetail(request, pk):
    bills = Bill.objects.get(pk=pk)
    items = lookup_items_bill(pk)
    cart= bills.billitems_set.first().cart
    clothe = items['clothe_bill']
    photo = items['photo_bill']
    makup = items['makup_bill']
    first_clothe = clothe[0][0]
    bill_total =get_total_values_bill(pk)
    total_retail = f"{bill_total['total_retail']:,}"
    discount = f"{bill_total['discount']:,}"
    incurred = f"{bill_total['incurred']:,}"
    total = f"{bill_total['total']:,}"
    paid = f"{bill_total['paid']:,}"
    receivable = f"{bill_total['receivable']:,}"
    template = loader.get_template('type_bill.html')
    context = {
        'bills':bills,
        'items':items,
        'clothe': clothe,
        'cart': cart ,
        'first_clothe': first_clothe,
        'total_retail': total_retail,
        'discount': discount,
        'incurred': incurred,
        'total': total,
        'paid' : paid,
        'receivable': receivable,
    }
    return HttpResponse(template.render(context, request))

