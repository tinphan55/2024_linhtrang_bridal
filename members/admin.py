from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from members.models import *
from django.utils.html import format_html

class MemberInline(admin.StackedInline):
    model = Member
    verbose_name_plural = 'member'
    can_delete = False
    #list_display = ["avatar","firstname", "lastname",'phone', 'joined_date']
    #search_fields = ["firstname", "lastname"]
    fields = ['avatar','phone', ]

class HRPoliciesInline(admin.StackedInline):
    model = HRPolicies
    can_delete = False

class RankingSetupAdmin(admin.ModelAdmin):
     models = RankingSetup




class CustomUserAdmin(UserAdmin):
    inlines = (MemberInline,HRPoliciesInline )
    list_display = ["image_tag","username","first_name", "last_name", "is_staff","ranking", "is_active"]
    list_display_links = ["username",]

    def image_tag(self, obj):
        member = Member.objects.filter(id_member_id =obj.id).first()
        if member is not None and member.avatar:
            return format_html('<img src="{}" style="border-radius: 50%; width: 40px; height: 40px; object-fit: cover;"/>'.format(member.avatar.url))
        else:
            return format_html('<img src="/media/member/default-image.jpg"style="border-radius: 50%; width: 40px; height: 40px; object-fit: cover;"/>')                   

    image_tag.short_description = 'avatar'

    def ranking(self, obj):
        item = HRPolicies.objects.filter(member = obj.pk).first()
        if item:
            ranking = item.ranking
        else:
            ranking = 'None'
        return ranking
    
class IncurredImcomeAdmin(admin.ModelAdmin):
    models = IncurredImcome
    fields = ('member', 'amount','month_period', 'year_period','description')
    
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(RankingSetup, RankingSetupAdmin)
admin.site.register(IncurredImcome, IncurredImcomeAdmin)

