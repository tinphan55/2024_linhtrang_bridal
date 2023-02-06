from django.contrib import admin
from django.contrib.auth.models import User
from .models import *
from import_export.admin import ImportExportModelAdmin
from .resources import ProductResource


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # Gợi ý trường slug theo category_name
    list_display = ('name','description')

class ClotheImportAdmin(ImportExportModelAdmin):
    resource_class = ProductResource

@admin.action(description='Confirm items is NOT available')   
def not_available (modeladmin, request, queryset):
    queryset.update(is_available = False )

class ClotheAdminView(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(ClotheAdminView, self).get_form(request, obj, **kwargs)
        form.base_fields['ranking'].queryset = Ranking.objects.filter(category=1)
        return form 
    list_display = ('code','name','ranking','qty','price', 'is_available','color')
    fields = ('code','name','ranking','qty', 'is_available','color','description','tags', 'images' )
    list_display_links = ('name',)
    search_fields = ('name','ranking', )
    readonly_fields =('category','price')
    actions = [not_available]


class ClotheAdmin(ClotheImportAdmin,ClotheAdminView ):
    pass

class PhotoAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(PhotoAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['ranking'].queryset = Ranking.objects.filter(category=2)
        return form 
    list_display = ('name','ranking','price', 'is_available')
    fields = ('name','ranking','price', 'is_available','description' ,'tags')
    list_display_links = ('name',)
    search_fields = ('name','ranking')
    readonly_fields =('category',)
    actions = [not_available]

class MakeupAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(MakeupAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['ranking'].queryset = Ranking.objects.filter(category=3)
        return form 
    list_display = ('name','ranking','price', 'is_available')
    fields = ('name','ranking','price', 'is_available','description', 'tags' )
    list_display_links = ('name',)
    search_fields = ('name','ranking')
    readonly_fields =('category',)
    actions = [not_available]

class AccessoryAdmin(admin.ModelAdmin):
    list_display = ('id','name','qty','price', 'is_available')
    fields = ('name','qty', 'is_available','price','description' , 'tags')
    list_display_links = ('name',)
    search_fields = ('name',)
    readonly_fields =('category',)
    actions = [not_available]

class RankingAdmin(admin.ModelAdmin):
    list_display = ('id','rank','price', 'category', 'description')
    search_fields = ('rank',)

#admin.site.register(ComboItem)
admin.site.register(Accessory, AccessoryAdmin)
admin.site.register(Makeup, MakeupAdmin)
admin.site.register(Clothe, ClotheAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
admin.site.register(Ranking,RankingAdmin )
