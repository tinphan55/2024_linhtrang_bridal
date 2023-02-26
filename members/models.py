from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Member(models.Model):
    id_member= models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phone = models.IntegerField(null=True)
    joined_date = models.DateField(null=True)
    avatar = models.ImageField(upload_to='member/', null = True, blank=True,default = None)

    def __str__(self):
        return super().__str__()
