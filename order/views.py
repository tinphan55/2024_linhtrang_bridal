from django.shortcuts import render
from django.views.generic.list import ListView
from django.http import HttpResponse
from django.template import loader
from order.models import ClotheService, AccessorysSerive
import datetime 
from order.forms import CheckProductsForm
from itertools import chain
from services_admin.function import available_qty_clothe_view, available_qty_accessory_view
from services_admin.models import Clothe, Accessory
from django.utils.dateformat import DateFormat
from django.http import Http404


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


from django.shortcuts import render

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






# def index(request):
#     code = request.GET.get('code')
#     start = request.GET.get('start')
#     end = request.GET.get('end')
#     days_list =[]
#     calendar = []
#     if code and start and end:
#         start_date = datetime.datetime.strptime(start, '%Y-%m-%d').date()
#         end_date = datetime.datetime.strptime(end, '%Y-%m-%d').date()
#         while start_date <= end_date:
#             calendar_item = {}
#             calendar_item['date'] = start_date.strftime('%Y-%m-%d')
#             pk = define_id(code)[0]
#             if pk is None:
#               t =  HttpResponse('<h1>Page was found</h1>')
#               break
#             else:
#               name = define_id(code)[1]
#               category = define_id(code)[2]
#               try: 
#                 calendar_item['qty_available'] = available_qty_clothe_view(pk, start_date)
#                 calendar.append(calendar_item)
#                 start_date += datetime.timedelta(days=1)
#               except calendar_item['qty_available'].DoesNotExist:
#                 try: 
#                   calendar_item['qty_available']= available_qty_accessory_view(pk, start_date)
#                   calendar.append(calendar_item)
#                   start_date += datetime.timedelta(days=1)
#                 except:
#                   calendar_item['qty_available'] = None
#     else:
#         raise Http404("No MyModel matches the given query.")
    
#     context = {
#         'form': CheckProductsForm,
#         'calendar': calendar,
#         'code': code,
#         'start': start,
#         'end': end,
#         'name': name,
#         'category': category,

#     }
   
#     return render(request, 'index.html', context)
   



      
  # #Hiển thị trong chuỗi cho tất cả các list clothe
  # elif start and end:
  #   pass
  

  # # Hiển thị cho duy nhất 1 mã cho trong chuỗi
  # elif code:
  #   pass

  # if date_check is None:
  #     date_check = datetime.today().strftime('%Y-%m-%d')
  # else:
  #     date_check = date_check

  # if code:
  #     clothes = clothes.filter(clothe__code=code)
  # if date_check:
  #     qty = available_qty_clothe(pk, date_check)
  # else:
  #     qty = 0

  