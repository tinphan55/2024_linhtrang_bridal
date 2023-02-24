from django.contrib import admin
from .models import *

# Register your models here.
class LayoutHomepageAdmin (admin.ModelAdmin):
    model = LayoutHomepage
    list_display =  ['id','block','is_menu','is_available',]
    
class BlockItemsAdmin (admin.ModelAdmin):
    model = LayoutHomepage
    list_display =  ['title','block','is_available','created_date']

admin.site.register(LayoutHomepage,LayoutHomepageAdmin)
admin.site.register(BlockItems, BlockItemsAdmin)