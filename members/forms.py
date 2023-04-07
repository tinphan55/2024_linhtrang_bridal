from django import forms
from datetime import date
from .models import *
import calendar


class CheckTimeForm(forms.Form):
    month = forms.ChoiceField(choices=[(str(i), str(i)) for i in range(1,13)])
    year = forms.IntegerField()