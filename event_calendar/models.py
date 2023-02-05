from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from order.models import Cart

title_choices = (
    ('photo', 'Chụp hình'),
    ('makeup', 'Trang điểm' ),
    ('take_photo', 'Lấy hình'),
    ('orther', 'Khác',),
)
class Event(models.Model):
    client = models.ForeignKey(Cart, on_delete= models.CASCADE)
    title = models.CharField(max_length=50, choices=title_choices)
    description = models.TextField(blank=True, null = True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return str(self.client)+ '_' + str (self.title)

    
    @property
    def get_html_url(self):
        url = reverse('event_calendar:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'