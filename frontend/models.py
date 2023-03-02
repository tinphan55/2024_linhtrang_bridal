from django.db import models


# Create your models here.
class LayoutHomepage(models.Model):
    block= models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)
    is_menu = models.BooleanField(default=True)
    def __str__(self):
        return str(self.block)

class BlockItems(models.Model):
    block = models.ForeignKey(LayoutHomepage, on_delete=models.CASCADE) 
    title = models.CharField(max_length=200)
    content = models.TextField(max_length= 500)
    images = models.ImageField(upload_to='frontend', default='', blank=True,null=True )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return str(self.title)
    
class CategoryDetail(models.Model):
    category =  models.ForeignKey(BlockItems, on_delete=models.CASCADE) 
    title = models.TextField(max_length= 500)
    images = models.ImageField(upload_to='frontend', default='', blank=True,null=True )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return str(self.title)


class ClientPotential(models.Model):
    service = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    phone = models.IntegerField()