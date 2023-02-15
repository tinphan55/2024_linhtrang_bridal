from django.urls import path
from . import views
app_name = 'bills'

urlpatterns = [
    path('bills/typebills/<int:pk>', views.billdetail, name='typebills'),
    
]