from django import forms
from datetime import datetime
import calendar

class DateForm(forms.Form):
    days_in_month = calendar.monthrange(datetime.now().year, datetime.now().month)
    days_list = range(1, days_in_month+1)
    #date_template = forms.CharField(widget=forms.TextInput())
    #dim_list = list(date_template for x in range(1, days_in_month[1]+1))
    #udělat jako dict, nebo list o 2 hodnotach (date a datum)
