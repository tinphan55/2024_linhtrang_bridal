from django.urls import path
from .views import *
app_name = 'bills'

urlpatterns = [
    path('bills/details/<int:pk>', billdetail, name='details'),
    #path('bills/pdf/<int:pk>', pdf, name = 'pdf'),
  
]