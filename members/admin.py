from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Member
from django.utils.html import format_html

class MemberInline(admin.StackedInline):
    model = Member
    verbose_name_plural = 'member'
    can_delete = False
    #list_display = ["avatar","firstname", "lastname",'phone', 'joined_date']
    #search_fields = ["firstname", "lastname"]
    fields = ['avatar','phone', ]


class CustomUserAdmin(UserAdmin):
    inlines = (MemberInline, )
    list_display = ["image_tag","username","first_name", "last_name", "is_staff", "is_active"]

    def image_tag(self, obj):
        member = Member.objects.filter(id_member_id =obj.id).first()
        if member.avatar:
            return format_html('<img src="{}" style="border-radius: 50%; width: 40px; height: 40px; object-fit: cover;"/>'.format(member.avatar.url))
        else:
            return format_html('<img src="/media/member/default-image.jpg"style="border-radius: 50%; width: 40px; height: 40px; object-fit: cover;"/>')                   

    image_tag.short_description = 'avatar'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

