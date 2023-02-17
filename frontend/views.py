from django.http import HttpResponse
from django.template import loader

def main(request):
  template = loader.get_template('frontend/home.html')
  return HttpResponse(template.render())