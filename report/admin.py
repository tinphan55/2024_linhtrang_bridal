from django.contrib import admin
from .models import *
# Register your models here.
class ReportAdmin(admin.ModelAdmin):
    list_display = ('name','url_link')
admin.site.register(Report, ReportAdmin)
