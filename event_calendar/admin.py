from django.contrib import admin
from .models import Event

# Register your models here.
class EventAdmin(admin.ModelAdmin):
    model= Event
    list_display =['client','title','start_time','end_time']
    list_filter = ['start_time','end_time','title']
admin.site.register(Event, EventAdmin)