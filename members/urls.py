from django.urls import path
from .views import *


urlpatterns = [
    path('salary', overview, name='overview'),
    path('salary/details/<int:pk>/<int:month>-<int:year>/', paycheck, name='paycheck'),

]