from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from order.models import Cart
from django.db.models.signals import post_save
from telegram import Bot
from infobot import *
from django.dispatch import receiver

title_choices = (
    ('photo', 'Chụp hình'),
    ('makeup', 'Trang điểm' ),
    ('take_photo', 'Lấy hình'),
    ('orther', 'Khác',),
)
class Event(models.Model):
    client = models.ForeignKey(Cart, on_delete= models.CASCADE, verbose_name="Khách hàng")
    title = models.CharField(max_length=50, choices=title_choices, verbose_name="Tiêu đề")
    description = models.TextField(blank=True, null = True, verbose_name="Mô tả")
    start_time = models.DateTimeField(verbose_name="Thời gian bắt đầu")
    end_time = models.DateTimeField(verbose_name="Thời gian kết thúc")

    class Meta:
        verbose_name = 'Lịch sự kiện'
        verbose_name_plural = 'Lịch sự kiện'

    def __str__(self):
        return str(self.client)+ '_' + str (self.title)

    
    @property
    def get_html_url(self):
        url = reverse('event_calendar:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'

@receiver(post_save, sender=Event)
def send_cart_message(sender, instance, created, **kwargs):
    if created:
        photo = Event.objects.get(pk =instance.pk )
        bot = Bot(token=bot_truong)
        if instance.title == 'photo':
            bot.send_message(
                chat_id=chat_group_id, 
                text= f"Hi Trường, có lịch chụp hình từ  {instance.start_time} đến {instance.end_time}")
            if instance.title =='makeup':
                bot.send_message(
                chat_id=chat_group_id, 
                text= f"Hi Linh, có lịch trang điểm từ  {instance.start_time} đến {instance.end_time}")  

