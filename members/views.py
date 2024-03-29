from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.models import User
from members.models import *
from django.db.models import Q, Count
from members.forms import *



# Create your views here.
def collect_cart_salary(info, month, year ):
    hr =[]
    for mem in info:
        item = {}
        cart = Cart.objects.filter(user=mem['member']).annotate(num_payments=Count('paymentschedulecart')).exclude(num_payments=0)
        cart_cal = [item for item in cart if item.receivable_raw == 0 
                    and item.latest_paid.month == month 
                    and item.latest_paid.year == year]
        incurred = IncurredImcome.objects.filter(member = mem['member'],
                        month_period = month,
                        year_period = year)
        total_incurred = sum(i.amount for i in incurred)
        total_clothe = sum(i.total_clothe for i in cart_cal)
        total_photo = sum(i.total_photo for i in cart_cal)
        total_makup = sum(i.total_makup for i in cart_cal)
        total_accessory = sum(i.total_accessory_hr for i in cart_cal)
        item['id'] = mem['member']
        item['first_name'] = mem['member__first_name']
        item['last_name']= mem['member__last_name']
        item['ranking'] = mem['ranking']
        item['salary'] = '{:,.0f}'.format( mem['salary'] )
        item['subsidize'] = '{:,.0f}'.format(mem['subsidize'])
        commission_clothe= mem['commission_clothe']* total_clothe
        item['total_clothe'] = '{:,.0f}'.format(total_clothe)
        item['total_photo']= '{:,.0f}'.format(total_photo)
        item['total_makup']='{:,.0f}'.format(total_makup)
        item['total_accessory'] = '{:,.0f}'.format(total_accessory)
        item['commission_clothe'] ='{:,.0f}'.format(commission_clothe)
        commission_photo = mem['commission_photo']*total_photo
        item['commission_photo']= '{:,.0f}'.format(commission_photo)
        commission_makup=mem['commission_makup']*total_makup
        item['commission_makup'] = '{:,.0f}'.format(commission_makup)
        commission_accesory = mem['commission_accesory']*total_accessory
        item['commission_accesory']='{:,.0f}'.format(commission_accesory)
        total  = commission_clothe+ commission_photo +commission_makup  + commission_accesory
        item['commission'] = '{:,.0f}'.format(total)
        item['incurred'] = '{:,.0f}'.format(total_incurred)
        item['imcome'] = '{:,.0f}'.format(mem['salary']+mem['subsidize']  +total_incurred+ total)
        hr.append(item)
    return hr

def myFunc(e):
  return e['imcome']



def overview(request):
    month = request.GET.get('month')
    year = request.GET.get('year')
    info = HRPolicies.objects.select_related('member').filter( Q(member__is_active=True)).values(
    'member', 'member__first_name', 'member__last_name', 'ranking', 'salary','subsidize',
    'commission_clothe', 'commission_makup','commission_photo','commission_accesory',
    'commission_accesory', 'commission_group')
    hr = []
    if month and year:
        month = int(month)
        year = int(year)
        hr = collect_cart_salary(info, month, year)
        hr.sort(reverse=True,key=myFunc)
    template = loader.get_template('paycheck/all_members.html')
    context = {
    'form': CheckTimeForm,
    'hr': hr,
        }
    return HttpResponse(template.render(context, request))

def paycheck(request, pk, month, year):
    info = HRPolicies.objects.select_related('member').filter( Q(member__is_active=True),Q(member=pk) ).values(
    'member', 'member__first_name', 'member__last_name', 'ranking', 'salary','subsidize',
    'commission_clothe', 'commission_makup','commission_photo','commission_accesory',
    'commission_accesory', 'commission_group')
    cart = Cart.objects.filter(
                    created_at__month=month,
                    created_at__year=year,
                    user = pk)
    cart = [item for item in cart if item.receivable_raw == 0]
    hr = collect_cart_salary(info,month, year)
    if len(hr)>0:
        hr = hr[0]
    template = loader.get_template('paycheck/paycheck.html')
    context = {
        'cart':cart,
        'hr': hr
    }
    return HttpResponse(template.render(context, request))