from django.http import HttpResponse
from django.template import loader
from frontend.models import *

#def difine_context()


def main(request):
  template = loader.get_template('frontend/home2.html')
  dashboard = BlockItems.objects.filter(block_id =1) 
  about_us = BlockItems.objects.filter(block_id =2) 
  service = BlockItems.objects.filter(block_id =3) 
  staff = BlockItems.objects.filter(block_id =4) 
  category = BlockItems.objects.filter(block_id =5) 
  news = BlockItems.objects.filter(block_id =6) 
  community = BlockItems.objects.filter(block_id =7) 
  phone = BlockItems.objects.filter(block_id =9, title = "Điện thoại")[0]
  address = BlockItems.objects.filter(block_id =9, title = "Địa chỉ")[0]
  email = BlockItems.objects.filter(block_id =9, title = "Email")[0]
  facebook = BlockItems.objects.filter(block_id =9, title = "Facebook")[0]
  ticktok = BlockItems.objects.filter(block_id =9, title = "Ticktok")[0]

 
  context ={
    "menu1":dashboard[0].block.block,
    "dash_1": dashboard[0].content,
    "dash_2": dashboard[1].content,
    "dash_3": dashboard[2].content,
    "menu2": about_us[0].block.block,
    "about_title" : about_us[0].title,
    "about_content" : about_us[0].content,
    "about_image" : about_us[0].images,
    "menu3": service[0].block.block,
    "ser1_title":service[0].title, 
    "ser2_title":service[1].title, 
    "ser3_title":service[2].title,
    "ser4_title":service[3].title,  
    "ser1_content":service[0].content, 
    "ser2_content":service[1].content, 
    "ser3_content":service[2].content, 
    "ser4_content":service[3].content, 
    "staff1_title":staff[0].title, 
    "staff2_title":staff[1].title, 
    "staff3_title":staff[2].title,
    "staff4_title": staff[3].title,  
    "staff1_content":staff[0].content, 
    "staff2_content":staff[1].content, 
    "staff3_content":staff[2].content, 
    "staff4_content":staff[3].content,
    "staff1_image":staff[0].images,
    "staff2_image":staff[1].images,
    "staff3_image":staff[2].images,
    "staff4_image":staff[3].images,
    "menu4": category[0].block.block,
    "category1_title":category[0].title, 
    "category2_title":category[1].title, 
    "category3_title":category[2].title, 
    "category1_content":category[0].content, 
    "category2_content":category[1].content, 
    "category3_content":category[2].content, 
    "menu5": news[0].block.block,
    "news1_title":news[0].title, 
    "news2_title":news[1].title, 
    "news3_title":news[2].title, 
    "news4_title":news[3].title, 
    "news1_content":news[0].content, 
    "news2_content":news[1].content, 
    "news3_content":news[2].content, 
    "news4_content":news[3].content,
    "com1_title":community[0].title, 
    "com2_title":community[1].title, 
    "com3_title":community[2].title, 
    "com1_content":community[0].content, 
    "com2_content":community[1].content, 
    "com3_content":community[2].content,
    "com1_image":community[0].images, 
    "com2_image":community[1].images, 
    "com3_image":community[2].images, 
    "menu6":phone.block.block,
    "phone": phone.content,
    "address": address.content,
    "mail": email.content,
    "face": facebook.content

    
  
  }
  return HttpResponse(template.render(context, request))