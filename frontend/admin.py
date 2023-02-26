from django.contrib import admin
from .models import *
from django.utils.html import format_html

# Register your models here.
class LayoutHomepageAdmin (admin.ModelAdmin):
    model = LayoutHomepage
    list_display =  ['id','block','is_menu','is_available',]
    list_display_links = ['block',]
    
class BlockItemsAdmin (admin.ModelAdmin):
    model = BlockItems
    list_display =  ['image_tag','title','block','is_available','created_date']
    fields = ['title','content','images','is_available']
    list_filter = ['block',]
    list_display_links = ['title',]

    def image_tag(self, obj):
        if obj.images:
            return format_html('<img src="{}" style=" width: 60px; height: 60px; object-fit: cover;"/>'.format(obj.images.url))
        else:
            return format_html('<img src="/media/member/default-image.jpg"style="border-radius: 50%; width: 40px; height: 40px; object-fit: cover;"/>')                   

    image_tag.short_description = 'image'

class CategoryDetailAdmin (admin.ModelAdmin):
    model = CategoryDetail
    list_display =  ['image_tag','title','category','is_available','created_date']
    fields = ['title','category','images','is_available']
    list_filter = ['category',]
    list_display_links = ['title',]

    def image_tag(self, obj):
        if obj.images:
            return format_html('<img src="{}" style=" width: 60px; height: 60px; object-fit: cover;"/>'.format(obj.images.url))
        else:
            return format_html('<img src="/media/member/default-image.jpg"style="border-radius: 50%; width: 40px; height: 40px; object-fit: cover;"/>')                   

    image_tag.short_description = 'image'


admin.site.register(LayoutHomepage,LayoutHomepageAdmin)
admin.site.register(BlockItems, BlockItemsAdmin)
admin.site.register(CategoryDetail, CategoryDetailAdmin)