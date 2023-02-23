from django.shortcuts import render
from .resources import ProductResource
from tablib import Dataset
from .models import *
from django.template import loader
from django.http import HttpResponse


def import_data(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        product_resource = ProductResource()
        dataset = Dataset()
        new_clothe = request.FILES['importData']

        if file_format == 'CSV':
            imported_data = dataset.load(new_clothe.read().decode('utf-8'),format='csv')
            result =  product_resource.import_data(dataset, dry_run=True)                                                                 
        elif file_format == 'JSON':
            imported_data = dataset.load(new_clothe.read().decode('utf-8'),format='json')
            # Testing data import
            result =  product_resource.import_data(dataset, dry_run=True) 

        if not result.has_errors():
            # Import now
            product_resource.import_data(dataset, dry_run=False)

    return render(request, 'import.html')    



