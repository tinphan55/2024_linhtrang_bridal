from django.urls import path
from . import views

urlpatterns = [
    path('checkproducts/', views.index, name='index'),
    path('gettodaycart/', views.todaycart, name='todaycart'),
]
