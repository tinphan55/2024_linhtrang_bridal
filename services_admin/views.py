from django.shortcuts import render
from .resources import ProductResource
from tablib import Dataset
from .models import Product
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


#demo load trang mới để xem
def products(request):
  myproducts = Product.objects.all().values()
  template = loader.get_template('all_products.html')
  context = {
    'myproducts': myproducts,
  }
  return HttpResponse(template.render(context, request))
#trang chi tiết
def details(request, id):
  myproducts = Product.objects.get(id=id)
  template = loader.get_template('details.html')
  context = {
     'myproducts': myproducts,
  }
  return HttpResponse(template.render(context, request))

