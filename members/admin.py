from django.contrib import admin
from .models import Member


class MemberAdmin(admin.ModelAdmin):
    list_display = ["firstname", "lastname",'phone', 'joined_date']
    search_fields = ["firstname", "lastname"]

# Register your models here.

admin.site.register(Member, MemberAdmin)