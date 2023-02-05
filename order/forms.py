from django import forms
from datetime import date

today = date.today()


class CheckProductsForm(forms.Form):
    code = forms.CharField()
    #date_check = forms.DateField(
    #    widget=forms.TextInput(attrs={'min': today, 'value': today, 'type': 'date'}), required=True)
   
    
    