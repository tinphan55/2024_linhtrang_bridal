from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    image = models.ImageField(upload_to='catagories/%Y/%m', null = True, blank=True,default = None)

    class Meta:
        verbose_name = 'Danh mục'
        verbose_name_plural = 'Danh mục'

    def __str__(self):
        return self.name


    
class Ranking (models.Model):
    rank = models.CharField(max_length=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    type = models.CharField(max_length=20, null=True, blank=True)
    description = models.CharField(max_length= 100, null=True, blank=True)
    price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    deposit = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.category) +'_' + str(self.type)+ '_' +str(self.rank)
    class Meta:
        verbose_name = 'Xếp hạng'
        verbose_name_plural = 'Xếp hạng'

class ItemBase (models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    ranking = models.ForeignKey(Ranking,on_delete=models.CASCADE, blank=True, null=True )
    price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    images = models.ImageField(upload_to='services_admin', default='', blank=True)
    is_available = models.BooleanField(default=True)   
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    deposit = models.IntegerField(default=0)
    tags = models.ManyToManyField('Tag', blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.category = Ranking.objects.get(id=self.ranking_id).category
        self.deposit = self.ranking.deposit
        #self.price = Ranking.objects.get(id=self.ranking_id).price
        super(ItemBase, self).save(*args, **kwargs)
    
class Clothe(ItemBase): 
    color =  models.CharField(max_length=20, null= True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    qty = models.IntegerField(null=False, default=1)
    code = models.CharField(max_length=10,null=False, blank=False, unique=True)

    class Meta:
        verbose_name = 'Quản lí Áo'
        verbose_name_plural = 'Quản lí Áo'
    
    def __str__(self):
        return self.code
    
    def save(self, *args, **kwargs):
        self.price = self.ranking.price
        self.discount = self.ranking.discount
        self.deposit = self.ranking.deposit
        super(ItemBase, self).save(*args, **kwargs)



class Photo(ItemBase):  
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=2)
    number_gate_photo = models.IntegerField()
    is_album=  models.BooleanField(default=False) 
    number_location = models.IntegerField()
    small_photo = models.IntegerField()
    origin_file = models.IntegerField()
    edit_file = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Quản lí chụp hình'
        verbose_name_plural = 'Quản lí chụp hình'

    

class Makeup(ItemBase):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=3)
    price = models.IntegerField()
    re_makup = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Quản lí trang điểm'
        verbose_name_plural = 'Quản lí trang điểm'
    
    
   
    
class Accessory(models.Model):
    name = models.CharField(max_length=50,null=False, blank=False, unique=True )
    ranking = models.ForeignKey(Ranking,on_delete=models.CASCADE, blank=True, null=True )
    qty = models.IntegerField(null=False)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=4)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', blank=True, null=True)
    is_sell = models.BooleanField(default=False)
    is_hr = models.BooleanField(default=False)
    deposit = models.IntegerField(default=0)
    #date_check = models.DateField(null = True, blank= True, default= datetime.now())
  
    class Meta:
        verbose_name = 'Quản lí phụ kiện'
        verbose_name_plural = 'Quản lí phụ kiện'
    def __str__(self):
        return self.name

@receiver(post_save, sender=Ranking)
def update_product(sender, instance, **kwargs):
    clothes = Clothe.objects.filter(ranking=instance)
    photos = Photo.objects.filter(ranking=instance)
    makups = Makeup.objects.filter(ranking=instance)
    for item in clothes:
        item.save()
    for item in photos:
        item.save()
    for item in makups:
        item.save()
    


class Tag (models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.name}"

class VolatilityAccessory (models.Model):
    product = models.ForeignKey(Accessory, on_delete = models.CASCADE, 
        limit_choices_to={'is_available': True})
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    qty = models.IntegerField(null=False)
    description = models.TextField(max_length=500, blank=True)

    class Meta:
        verbose_name = 'Quản lí xuất nhập sản phẩm'
        verbose_name_plural = 'Quản lí xuất nhập sản phẩm'

