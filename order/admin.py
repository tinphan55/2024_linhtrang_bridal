from django.utils.html import format_html
from services_admin import *
from django.contrib import admin
from order.models import *
from django.db.models import  Sum
from event_calendar.models import Event
from datetime import datetime, timedelta, date

from order.forms import *
from django.db.models import Q
from members.models import Member
from dateutil.relativedelta import relativedelta
from services_admin.function import *



class ClotheServiceInline(admin.StackedInline):
    form = ClotheServiceForm
    model= ClotheService
    fields = ['clothe','qty','is_discount','delivery_date','return_date','total_items_','total_deposit_str']
    readonly_fields = ['total_items_','total_deposit_str']
    from datetime import timedelta

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "clothe":
            cart_id = request.resolver_match.kwargs.get('object_id')
            clothe = Clothe.objects.filter(is_available=True)
            if cart_id:
                cart = Cart.objects.get(pk=cart_id)
                selected_clothes = Clothe.objects.filter(clotheservice__cart=cart) 
                wed1 = cart.wedding_date
                wed2 = cart.wedding_date_2
                INFINITY_DATE = date.max
                MINUS_INFINITY_DATE = date.min
                max_wedding = max(wed1 or MINUS_INFINITY_DATE, wed2 or MINUS_INFINITY_DATE)
                min_wedding = min(wed1 or INFINITY_DATE, wed2 or INFINITY_DATE)
                delivery = min_wedding - timedelta(days=2)
                receive = max_wedding + timedelta(days=2) 
                check_date = [delivery, min_wedding, max_wedding, receive]
                # Tạo một danh sách các pk của các Clothe có sẵn và đáp ứng điều kiện
                available_clothe_pks = [
                    item.pk for item in clothe 
                    if all(available_qty_clothe_view(item.pk, date) > 0 for date in check_date)
                ]
                # Tạo queryset kết hợp giữa selected_clothes và clothe
                combined_queryset = (selected_clothes | clothe.filter(pk__in=available_clothe_pks)).distinct()
                kwargs["queryset"] = combined_queryset
            else:
                kwargs["queryset"] = Clothe.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    

        

    @admin.display(description='Tổng tiền')
    def total_items_(self,obj):
        return obj.str_total_items
    
    @admin.display(description='Đặt cọc')
    def total_deposit_str(self,obj):
        return '{:,.0f}'.format( obj.total_deposit)
    
@admin.action(description='Xác nhận sản phẩm được trả')
def confirm_returned(modeladmin, request, queryset):
    for return_item in queryset:
        if not return_item.is_returned:
            return_item.is_returned = True
            return_item.returned_at = datetime.now()
            return_item.save()
    
@admin.action(description='Hủy trả sản phẩm')
def confirm_not_returned(modeladmin, request, queryset):
    for return_item in queryset:
        if return_item.is_returned:
            return_item.is_returned = False
            return_item.returned_at = None
            return_item.save()


class ItemStatusFilter(admin.SimpleListFilter):
    title = 'Tình trạng cho thuê'
    parameter_name = 'item_status'

    def lookups(self, request, model_admin):
        return (
            ('Chờ cho thuê', 'Chờ cho thuê'),
            ('Đang cho thuê', 'Đang cho thuê'),
            ('Quá hạn thuê', 'Quá hạn thuê'),
            ('Đã thu hồi', 'Đã thu hồi'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'Chờ cho thuê':
            return queryset.filter(delivery_date__gt=date.today())
        elif self.value() == 'Đang cho thuê':
            return queryset.filter(delivery_date__lte=date.today(), returned_at__isnull=True, return_date__gte=date.today())
        elif self.value() == 'Quá hạn thuê':
            return queryset.filter(delivery_date__lte=date.today(), returned_at__isnull=True, return_date__lt=date.today())
        elif self.value() == 'Đã thu hồi':
            return queryset.filter(returned_at__isnull=False)
        

class WeddingDateFilter(admin.SimpleListFilter):
    title = 'Chọn ngày cưới'
    parameter_name = 'wedding_date'

    def lookups(self, request, model_admin):
        return (
            ('this_month', 'This month'),
            ('next_month', 'Next month'),
            ('next_2_months', 'Next 2 months'),
            ('next_3_months', 'Next 3 months'),
            # ('custom', 'Custom'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'this_month':
            return queryset.filter(cart__wedding_date__month=date.today().month)
        elif self.value() == 'next_month':
            next_month = date.today().replace(day=28) + timedelta(days=4)
            next_month = next_month.replace(day=1)
            return queryset.filter(cart__wedding_date__month=next_month.month, cart__wedding_date__year=next_month.year)
        elif self.value() == 'next_2_months':
            next_month = date.today().replace(day=28) + timedelta(days=4)
            next_month = next_month.replace(day=1)
            next_2_months = next_month + relativedelta(months=1)
            return queryset.filter(cart__wedding_date__gte=next_month, cart__wedding_date__lt=next_2_months)
        elif self.value() == 'next_3_months':
            next_month = date.today().replace(day=28) + timedelta(days=4)
            next_month = next_month.replace(day=1)
            next_3_months = next_month + relativedelta(months=2)
            return queryset.filter(cart__wedding_date__gte=next_month, cart__wedding_date__lt=next_3_months)
        elif self.value() == 'custom':
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            if start_date and end_date:
                return queryset.filter(cart__wedding_date__range=(start_date, end_date))
        return queryset



class ReturnClotheAdmin(admin.ModelAdmin):
    def clothe_id(self, obj):
        return obj.clothe.id
    model = ReturnClothe
    list_display = ('cart','clothe','type_clothe','name_clothe','qty' ,'delivery_date', 'return_date',  'returned_at', 'item_status')
    fields = ['clothe','qty', 'delivery_date', 'return_date', 'is_returned',  'returned_at','note']
    readonly_fields = ['clothe','qty', 'delivery_date', 'return_date','item_status','is_returned', 'returned_at',]
    list_display_links = ('clothe',)
    list_filter =  ('is_returned' ,WeddingDateFilter,'clothe__ranking__type',ItemStatusFilter)
    search_fields = ( 'cart__client__phone', 'cart__id', 'clothe__code')
    actions = [confirm_returned, confirm_not_returned]
    admin.site.disable_action('delete_selected')
    @admin.display(description='color_')
    def get_color(self, obj):
        return obj.clothe.color
    def type_clothe(self, obj):
        return obj.clothe.ranking.type
    def name_clothe(self, obj):
        return obj.clothe.name
    type_clothe.short_description = 'Mã áo'
    name_clothe.short_description = 'Tên áo'

    
    

    
class ReturnAccessoryAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(product__is_sell=False)
    model = ReturnAccessory
    list_display = ('cart','product','qty' ,'delivery_date', 'return_date','returned_at' , 'item_status' )
    fields = ['product','qty', 'delivery_date', 'return_date',  'returned_at','note', ]
    readonly_fields = ['product','qty', 'delivery_date', 'return_date','returned_at',]
    list_display_links = ('product',)
    list_filter =  ('is_returned', WeddingDateFilter , ItemStatusFilter)
    search_fields = ( 'cart__client__phone', 'cart__id', 'product__name')
    actions = [confirm_returned, confirm_not_returned]
   

class PhotoScheduleInline(admin.StackedInline):
    model =  Event 
    extra = 1
    fields = ['title','start_time','end_time','description']
    
   

class MakeupServiceInline(admin.StackedInline):
    model =  MakeupService
    fields = ['package','note','is_discount','total_items_','total_deposit_str']
    #raw_id_fields = ['product']
    readonly_fields = ['total_items_','total_deposit_str']
    extra = 1
    @admin.display(description='Tổng tiền')
    def total_items_(self,obj):
        return obj.str_total_items
    
    @admin.display(description='Đặt cọc')
    def total_deposit_str(self,obj):
        return '{:,.0f}'.format( obj.total_deposit)
    

class AccessoryServiceInline(admin.StackedInline):
    model =  AccessorysSerive
    fields = ['product','qty','is_discount','total_items_', 'delivery_date', 'return_date','total_deposit_str']
    #raw_id_fields = ['product']
    readonly_fields = ['total_items_','total_deposit_str']
    @admin.display(description='Tổng tiền')
    def total_items_(self,obj):
        return obj.str_total_items
    @admin.display(description='Đặt cọc')
    def total_deposit_str(self,obj):
        return '{:,.0f}'.format( obj.total_deposit)
    

    
    

class PhotoServiceInline(admin.StackedInline):
    model = PhotoService 
    fields = ['package','is_discount','note','total_items_','total_deposit_str']
    readonly_fields = ['total_items_', 'total_deposit_str']
    extra = 1
    @admin.display(description='Tổng tiền')
    def total_items_(self,obj):
        return obj.str_total_items
    @admin.display(description='Đặt cọc')
    def total_deposit_str(self,obj):
        return '{:,.0f}'.format( obj.total_deposit)
    


class IncurredCartInline(admin.StackedInline):
    form = IncurredCartForm
    model = IncurredCart 
    extra = 1 
    fields = ['amount','description','created_at']

class PaymentCartInline(admin.StackedInline):
    model = PaymentScheduleCart
    extra = 3 
    fields = ['amount','description','created_at']
   
        



class CartAdmin(admin.ModelAdmin):
    model= Cart 
    form = CartForm
    list_display=('id','image_tag','user','client','created_at', 'total_cart','total_discount', 'total_incurred', 'total', 'paid_','receivable_','total_deposit', 'wedding_date','wedding_date_2')
    fields = ['client','wedding_date','wedding_date_2','note','total_cart', 'total_discount','total_incurred', 'total','paid_', 'receivable_','total_deposit']
    list_display_links=('client',)
    search_fields=('client__phone',)
     #['created_at','wedding_date',]
    readonly_fields = [ 'created_at','total_cart','total_discount', 'total_incurred', 'total', 'paid_','receivable_','total_deposit']
    list_filter = ('created_at','user__username', 'client__full_name')
    inlines = [PaymentCartInline,ClotheServiceInline,PhotoServiceInline, MakeupServiceInline, AccessoryServiceInline,IncurredCartInline,PhotoScheduleInline]
    

    def save_model(self, request, obj, form, change):
        # Override phương thức save_model để tự động lưu trường user là người dùng đang đăng nhập
        obj.user = request.user
        obj.save()

    def image_tag(self, obj):
        member = Member.objects.filter(id_member_id =obj.user_id).first()
        if member is not None and member.avatar:
            return format_html('<img src="{}" style="border-radius: 50%; width: 40px; height: 40px; object-fit: cover;"/>'.format(member.avatar.url))
        else:
            return format_html('<img src="/media/member/default-image.jpg"style="border-radius: 50%; width: 40px; height: 40px; object-fit: cover;"/>')                   

    image_tag.short_description = 'avatar'

    @admin.display(description='Tổng trước giảm')
    def total_cart(self, obj):
        return '{:,.0f}'.format(obj.total_cart_raw)

    @admin.display(description='Tổng phát sinh')
    def total_incurred(self, obj):
        return '{:,.0f}'.format(obj.total_incurred_raw)
    @admin.display(description='Tổng giảm')
    def total_discount (self, obj):
        return '{:,.0f}'.format(obj.total_discount_raw)
    
    @admin.display(description='Tổng sau giảm')
    def total(self, obj):
        return '{:,.0f}'.format(obj.total_raw)

    @admin.display(description='Tổng trả')
    def paid_(self, obj):
        return '{:,.0f}'.format(obj.total_payment_raw)

    @admin.display(description='Cần thu')
    def receivable_(self, obj):
        return'{:,.0f}'.format(obj.receivable_raw)
    
    @admin.display(description='Cần đặt cọc')
    def total_deposit(self, obj):
        return'{:,.0f}'.format(obj.total_deposit_raw)

    
    

   

admin.site.register(Cart,CartAdmin )
admin.site.register(ReturnClothe, ReturnClotheAdmin)
admin.site.register(ReturnAccessory,ReturnAccessoryAdmin)

