from django.shortcuts import render
from django.views.generic.list import ListView
from django.http import HttpResponse
from django.template import loader
from .models import *
import datetime
from .forms import CheckProductsForm



def index(request):
  code = request.GET.get('code')
  #date_check = request.GET.get('date_check')
  clothes = ClotheService.objects.all()
  if code :#and date_check:
    clothes = clothes.filter(clothe__code = code)#, delivery_date__lte = date_check ,
     #return_date__gte=date_check ).order_by('-delivery_date')
  context = {
    'form': CheckProductsForm,
    'clothes':clothes
  }
  return render(request, 'index.html', context)