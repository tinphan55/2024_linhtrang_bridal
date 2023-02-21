from order.models import *
from services_admin.models import *
from django.db.models import Sum
from datetime import datetime


def available_qty_accessory_admin(pk, date_check):
    item = Accessory.objects.get(pk=pk)
    start_date = item.created_date
    qty_begin = item.qty
    item.is_sell
    end_date = datetime.now()
    is_sell = item.is_sell
    if item.is_sell == True:
        order_qty = AccessorysSerive.objects.filter(product__id=pk, created_at__lt=end_date, created_at__gt=start_date).aggregate(Sum('qty'))['qty__sum']
        if order_qty is not None:
            order_qty = order_qty
        else:
            order_qty= 0
        volatility_qty = VolatilityAccessory.objects.filter(product__id=pk, created_date__lt=end_date, created_date__gt=start_date).aggregate(Sum('qty'))['qty__sum']
        if volatility_qty is not None:
            volatility_qty = volatility_qty
        else:
            volatility_qty= 0
    else:
        order_qty = AccessorysSerive.objects.filter(product__id=pk, delivery_date__lt= date_check, delivery_date__gt=start_date).aggregate(Sum('qty'))['qty__sum']
        if order_qty is not None:
            order_qty = order_qty
        else:
            order_qty= 0
        volatility_qty = AccessorysSerive.objects.filter(product__id=pk,returned_at__lt= date_check, returned_at__gt=start_date).aggregate(Sum('qty'))['qty__sum']
        if volatility_qty is not None:
            volatility_qty = volatility_qty
        else:
            volatility_qty = 0

    qty_available =  qty_begin +  volatility_qty - order_qty
    return qty_available, qty_begin, volatility_qty, order_qty



def available_qty_clothe_admin(pk, date_check):
    item = Clothe.objects.get(pk=pk)
    start_date = item.created_date.strftime('%Y-%m-%d')
    qty_begin = item.qty
    order_qty = ClotheService.objects.filter(clothe__id=pk, delivery_date__lte= date_check, delivery_date__gte=start_date).aggregate(Sum('qty'))['qty__sum']
    if order_qty is not None:
        order_qty = order_qty
    else:
        order_qty= 0
    volatility_qty = ClotheService.objects.filter(
        clothe__id=pk,
        returned_at__lte=date_check,
        returned_at__gte=start_date
            ).aggregate(Sum('qty'))['qty__sum']
    if volatility_qty is not None:
        volatility_qty = volatility_qty
    else:
        volatility_qty = 0
    qty_available =  qty_begin +  volatility_qty - order_qty
    return qty_available, volatility_qty, order_qty

def available_qty_clothe_view(pk, date_check):
    item = Clothe.objects.get(pk=pk)
    start_date = item.created_date
    qty_begin = item.qty
    order_qty = ClotheService.objects.filter(
        clothe__id=pk, 
        delivery_date__lte= date_check, 
        delivery_date__gte= start_date
            ).aggregate(Sum('qty'))['qty__sum']
    if order_qty is not None:
        order_qty = order_qty
    else:
        order_qty= 0
    volatility_qty = ClotheService.objects.filter(
        clothe__id=pk,
        return_date__lte=date_check,
        return_date__gte=start_date
            ).aggregate(Sum('qty'))['qty__sum']
    if volatility_qty is not None:
        volatility_qty = volatility_qty
    else:
        volatility_qty = 0
    qty_available =  qty_begin +  volatility_qty - order_qty
    return qty_available

def available_qty_accessory_view(pk, date_check):
    item = Accessory.objects.get(pk=pk)
    start_date = item.created_date
    qty_begin = item.qty
    item.is_sell
    end_date = datetime.now()
    is_sell = item.is_sell
    if item.is_sell == True:
        order_qty = AccessorysSerive.objects.filter(product__id=pk, created_at__lt=end_date, created_at__gt=start_date).aggregate(Sum('qty'))['qty__sum']
        if order_qty is not None:
            order_qty = order_qty
        else:
            order_qty= 0
        volatility_qty = VolatilityAccessory.objects.filter(product__id=pk, created_date__lt=end_date, created_date__gt=start_date).aggregate(Sum('qty'))['qty__sum']
        if volatility_qty is not None:
            volatility_qty = volatility_qty
        else:
            volatility_qty= 0
    else:
        order_qty = AccessorysSerive.objects.filter(
            product__id=pk, 
            delivery_date__lte= date_check, 
            delivery_date__gte=start_date
                ).aggregate(Sum('qty'))['qty__sum']
        if order_qty is not None:
            order_qty = order_qty
        else:
            order_qty= 0
        volatility_qty = AccessorysSerive.objects.filter(
            product__id=pk,
            return_date__lte= date_check, 
            return_date__gte =start_date
                ).aggregate(Sum('qty'))['qty__sum']
        if volatility_qty is not None:
            volatility_qty = volatility_qty
        else:
            volatility_qty = 0

    qty_available =  qty_begin +  volatility_qty - order_qty
    return qty_available
