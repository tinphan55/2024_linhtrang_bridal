from django.shortcuts import render
from django.views.generic.list import ListView
from django.http import HttpResponse
from django.template import loader
from order.models import *
import datetime 
from order.forms import CheckProductsForm
from itertools import chain
from services_admin.function import available_qty_clothe_view, available_qty_accessory_view
from services_admin.models import Clothe, Accessory
from django.utils.dateformat import DateFormat
from django.http import Http404
from django.http import JsonResponse
from django.db.models import Q


def define_id(code):
  try:
    obj = Accessory.objects.get(name=code)
    pk = obj.id
    name = obj.name
    category = obj.category.name
  except Accessory.DoesNotExist:
    try:
        obj = Clothe.objects.get(code=code)
        pk = obj.id
        name = obj.name
        category = obj.category.name
    except Clothe.DoesNotExist:
        pk = None
  return pk, name, category




def index(request):
    code = request.GET.get('code')
    start = request.GET.get('start')
    end = request.GET.get('end')
    days_list =[]
    calendar = []
    name = None
    category = None
    if code and start and end:
        try:
            obj_id, name, category = define_id(code)
            if obj_id is None:
                return render(request, 'error.html')
            else:
                start_date = datetime.datetime.strptime(start, '%Y-%m-%d').date()
                end_date = datetime.datetime.strptime(end, '%Y-%m-%d').date()
                while start_date <= end_date:
                    calendar_item = {'date': start_date.strftime('%Y-%m-%d')}
                    try:
                        calendar_item['qty_available'] = available_qty_clothe_view(obj_id, start_date)
                    except (AttributeError, DoesNotExist):
                        try:
                            calendar_item['qty_available'] = available_qty_accessory_view(obj_id, start_date)
                        except:
                            calendar_item['qty_available'] = None
                    calendar.append(calendar_item)
                    start_date += datetime.timedelta(days=1)
        except:
            return render(request, 'error.html')
    # else:
    #     return render(request, 'error.html')

    context = {
        'form': CheckProductsForm,
        'calendar': calendar,
        'code': code,
        'start': start,
        'end': end,
        'name': name,
        'category': category,
    }
    return render(request, 'index.html', context)



def todaycart(request):
    start_of_day = datetime.datetime.combine(datetime.datetime.now().date(), datetime.time.min)
    end_of_day = datetime.datetime.combine(datetime.datetime.now().date(), datetime.time.max)
    cart = Cart.objects.filter(
        Q(created_at__gte=start_of_day) & Q(created_at__lte=end_of_day)
            )
    total_cart = sum(i.total_raw for i in cart)
    total_paid = sum(i.total_payment_raw for i in cart)
    response_data = {
        'total_cart': '{:,.0f}'.format(total_cart),
        'total_paid': '{:,.0f}'.format(total_paid)
    }
    return JsonResponse(response_data)