from django.urls import path
from . import views
app_name = 'bills'

urlpatterns = [
    path('bills/details/<int:pk>', views.billdetail, name='details'),
  
   
]