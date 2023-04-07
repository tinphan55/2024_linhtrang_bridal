from django.shortcuts import render
from django.http import HttpResponse
from bills.function import *
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Image, Spacer
from django.template.loader import get_template
from reportlab.lib.units import cm




def billdetail(request, pk):
    template = loader.get_template('bills/bill2.html')
    context = context_bill(pk)
    return HttpResponse(template.render(context, request))

# def pdf(request, pk):
#     bills = Bill.objects.get(pk=pk)
#     template = loader.get_template('bills/bill2.html')
#     context = context_bill(pk)
#     html = template.render(context, request)
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'filename=bill_{pk}.pdf'
#     pisa.CreatePDF(html, dest=response, link_callback=fetch_resources)
#     return response


