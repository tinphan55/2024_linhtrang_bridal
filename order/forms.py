from django import forms
from datetime import date
from .models import *
from django.forms import CharField, ModelForm
from services_admin.models import *
from django.utils.translation import gettext_lazy as _

today = date.today()

class CheckProductsForm(forms.Form):
    code = forms.CharField()
    start = forms.DateField(
        widget=forms.TextInput(attrs={
            'type': 'date',
        }),
        initial=date.today() + timedelta(days=30),
        required=True
    )
    end = forms.DateField(
        widget=forms.TextInput(attrs={
            'type': 'date',
        }),
        initial=date.today() + timedelta(days=60),
        required=True
    )





class CartForm(ModelForm):
    class Meta:
        model = Cart
        fields = ('user','client','wedding_date','note')
        help_texts = {
            'user': _('Nhập nhân viên tạo đơn'),
            'client': _('Kiểm tra Khách hàng đã có chưa hoặc tạo mới KH') , 
            'note': _('Thêm yêu cầu của KH nếu có')}

class IncurredCartForm(ModelForm):
    class Meta:
        models = IncurredCart
        fields = ('amount','description','created_at')
        help_texts = {
            'amount': _('Phát sinh: Nếu phát sinh tăng thì nhập dương, phát sinh giảm thì nhập âm "-"'),
            'description': _('Mô tả chi tiết về sự kiện phát sinh')  }

class ClotheServiceForm(ModelForm):
    class Meta:
        models = ClotheService    
        fields = ('clothe','qty','discount','delivery_date','return_date' )
        help_texts = {
            'clothe':  _('Chọn quần áo'),
            'discount': _('Giảm giá: Nếu có giảm giá thì nhập vào'),
            'delivery_date': _('Ngày cho thuê đồ: Nếu có thay đổi thì nhập, mặc định trước 2 ngày cưới'),
            'return_date' : _('Ngày trả đồ: Nếu có thay đổi thì nhập, mặc định sau 2 ngày cưới'),   }

class IncurredCartForm(ModelForm):
    class Meta:
        models = IncurredCart    
        fields = ('amount','description','created_at')
        help_texts = {
            'amount': _('Phát sinh: Nếu phát sinh tăng thì nhập dương, phát sinh giảm thì nhập âm "-"'),
            'description': _('Mô tả chi tiết về sự kiện phát sinh')  }
