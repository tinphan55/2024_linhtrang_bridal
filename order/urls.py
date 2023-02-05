from django.urls import path
from . import views

urlpatterns = [
    path('checkproducts/', views.index, name='index'),
]
