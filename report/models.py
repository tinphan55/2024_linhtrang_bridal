from django.db import models
from django.contrib.auth.models import Group
from django.utils.html import format_html

class Report(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def url_link(self):
       return format_html('<a href="%s" target="_blank">%s</a>' % (self.url, "Xem báo cáo"))
    url_link.short_description = 'URL' # tên cột trong Django admin

    class Meta:
        verbose_name = 'Báo cáo'
        verbose_name_plural = 'Báo cáo'
