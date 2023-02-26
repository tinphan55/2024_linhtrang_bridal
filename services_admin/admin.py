from django.contrib import admin
from django.contrib.auth.models import User
from .models import *
from import_export.admin import ImportExportModelAdmin
from .resources import ProductResource
from services_admin.function import *
from django.utils.html import format_html




class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # Gợi ý trường slug theo category_name
    list_display = ('id','name','description')

class ClotheImportAdmin(ImportExportModelAdmin):
    resource_class = ProductResource

@admin.action(description='Xác nhận sản phẩm KHÔNG còn khả dụng')   
def not_available (modeladmin, request, queryset):
    queryset.update(is_available = False )

class ClotheAdminView(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(ClotheAdminView, self).get_form(request, obj, **kwargs)
        form.base_fields['ranking'].queryset = Ranking.objects.filter(category=1)
        return form 
    list_display = ('code','name','ranking','available_qty','return_qty','order_qty','price', 'discount','is_available','color')
    fields = ('code','name','ranking','qty', 'is_available','color','description','tags' )
    list_display_links = ('name',)
    search_fields = ('code', )
    readonly_fields =('category','price')
    list_filter = ('ranking','is_available', )
    actions = [not_available]
    #Đúng
    def available_qty(self, obj):
         date_check = datetime.now()
         qty = available_qty_clothe_admin(obj.pk,date_check )
         return qty[0]
    #đúng
    def return_qty(self, obj):
         date_check = datetime.now()
         qty = available_qty_clothe_admin(obj.pk,date_check)
         return qty[1]
    #đúng
    def order_qty(self, obj):
         date_check = datetime.now()
         qty = available_qty_clothe_admin(obj.pk,date_check)
         return qty[2]


class ClotheAdmin(ClotheImportAdmin,ClotheAdminView ):
    pass

class PhotoAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(PhotoAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['ranking'].queryset = Ranking.objects.filter(category=2)
        return form 
    list_display = ('name','ranking','number_location','number_gate_photo','small_photo','origin_file','edit_file', 'is_album','price','discount', 'is_available')
    fields = ('name','ranking','number_location','number_gate_photo','small_photo','origin_file','edit_file','is_album','price','discount', 'is_available','description' ,'tags')
    list_display_links = ('name',)
    search_fields = ('name',)
    readonly_fields =('category',)
    actions = [not_available]
    

class MakeupAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(MakeupAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['ranking'].queryset = Ranking.objects.filter(category=3)
        return form 
    list_display = ('name','ranking','re_makup','price','discount', 'is_available')
    fields = ('name','ranking','re_makup','price','discount', 'is_available','description', 'tags' )
    list_display_links = ('name',)
    search_fields = ('name',)
    readonly_fields =('category',)
    actions = [not_available]


class AccessoryAdmin(admin.ModelAdmin):
     def get_form(self, request, obj=None, **kwargs):
         form = super(AccessoryAdmin, self).get_form(request, obj, **kwargs)
         form.base_fields['ranking'].queryset = Ranking.objects.filter(category=4)
         return form 
     list_display = ('id','name','ranking','is_sell','price','discount','qty_available','qty_add','qty_order', 'is_available')
     fields = ('name','ranking','is_sell','qty','price', 'discount','is_available','description' , 'tags')
     list_display_links = ('name',)
     search_fields = ('name',)
     list_filter=('is_sell',)
     readonly_fields =('category',)
     actions = [not_available]
     def qty_available(self, obj):
         date_check = datetime.now()
         qty = available_qty_accessory_admin(obj.pk,date_check )
         return qty[0]
     def qty_add(self, obj):
         date_check = datetime.now()
         qty = available_qty_accessory_admin(obj.pk,date_check )
         return qty[2]
     def qty_order(self, obj):
         date_check = datetime.now()
         qty = available_qty_accessory_admin(obj.pk,date_check )
         return qty[3]
    






   
# class VolatilityAccessoryAdmin(admin.ModelAdmin):
#     pass

class RankingAdmin(admin.ModelAdmin):
    list_display = ('id','rank','type','price','discount', 'category', 'description')
    list_display_links = ('id', 'rank')
    list_filter = ('category',)
    search_fields = ('rank',)

class VolatilityAccessoryAdmin(admin.ModelAdmin):
    model = VolatilityAccessory
    list_display = ('product','created_date','qty',)



admin.site.register(VolatilityAccessory ,VolatilityAccessoryAdmin)
admin.site.register(Accessory, AccessoryAdmin)
admin.site.register(Makeup, MakeupAdmin)
admin.site.register(Clothe, ClotheAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
admin.site.register(Ranking,RankingAdmin )




    