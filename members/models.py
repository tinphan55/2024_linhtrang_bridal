from django.db import models
from django.contrib.auth.models import User
from order.models import *


class RankingSetup(models.Model):
    PARTNER_CHOICES = (
        ('1', 'Thử việc'),
        ('2', 'Nhân viên'),
        ('3', 'Chuyên viên'),
        ('4', 'Trưởng nhóm'),
        ('5', 'Trưởng phòng'),
        ('6', 'Giám đốc khối '),
        ('7', 'Tổng giám đốc '),)
    ranking = models.CharField(max_length=10, choices=PARTNER_CHOICES, unique=False, 
                               verbose_name='Cấp nhân viên')
    description = models.CharField(max_length=250, verbose_name='Mô tả')
    created_at = models.DateTimeField(default=datetime.now, verbose_name='Ngày tạo')
    salary = models.FloatField(verbose_name='Lương cơ bản')
    commission_clothe = models.FloatField(verbose_name='Hoa hồng thuê đồ')
    commission_makup = models.FloatField(verbose_name='Hoa hồng trang điểm')
    commission_photo = models.FloatField(verbose_name='Hoa hồng chụp hình')
    commission_accesory = models.FloatField(verbose_name='Hoa hồng phụ kiện')
    commission_group = models.FloatField(verbose_name='Hoa hồng nhóm')
    subsidize = models.FloatField(default=0, verbose_name='Trợ cấp')
    is_available = models.BooleanField(default=True, verbose_name='Khả dụng')
    class Meta:
        verbose_name = 'Thiết lập Cấp bật nhân viên'
        verbose_name_plural = 'Thiết lập Cấp bật nhân viên'

    def __str__(self):
        return self.ranking

@receiver(post_save, sender=RankingSetup)
def update_hr_policies(sender, instance, **kwargs):
    items = HRPolicies.objects.filter(ranking=instance)
    for item in items:
        item.save()
    


    




# Create your models here.
class Member(models.Model):
    id_member= models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phone = models.IntegerField(null=True)
    joined_date = models.DateField(null=True)
    avatar = models.ImageField(upload_to='member', null = True, blank=True,default = "")
    
    class Meta:
        verbose_name = 'Cập nhật thêm thông tin(bắc buộc)'
        verbose_name_plural = 'Cập nhật thêm thông tin(bắc buộc)'
    
    def __str__(self):
        return self.id_member.username

class HRPolicies(models.Model):
    member = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    ranking = models.ForeignKey(RankingSetup, on_delete = models.CASCADE,
        limit_choices_to={'is_available': True}, verbose_name='Cấp nhân viên')
    salary = models.FloatField(default=0, verbose_name='Lương cơ bản')
    commission_clothe = models.FloatField(default=0, verbose_name='Hoa hồng thuê đồ')
    commission_makup = models.FloatField(default=0, verbose_name='Hoa hồng trang điểm')
    commission_photo = models.FloatField(default=0, verbose_name='Hoa hồng chụp hình')
    commission_accesory = models.FloatField(default=0, verbose_name='Hoa hồng phụ kiện')
    commission_group = models.FloatField(default=0, verbose_name='Hoa hồng nhóm')
    subsidize = models.FloatField(default=0, verbose_name='Trợ cấp')
    created_at = models.DateTimeField(default=datetime.now)
    class Meta:
        verbose_name = 'Thiếp lập cấp nhân viên'
        verbose_name_plural = 'Thiếp lập cấp nhân viên'

    def __str__(self):
        return self.member.username
    
    def save(self, *args, **kwargs):
        self.salary = self.ranking.salary
        self.commission_clothe = self.ranking.commission_clothe
        self.commission_photo = self.ranking.commission_photo
        self.commission_accesory = self.ranking.commission_accesory
        self.commission_makup = self.ranking.commission_makup
        self.commission_group = self.ranking.commission_group
        self.subsidize = self.ranking.subsidize
        super(HRPolicies, self).save(*args, **kwargs)
    
class IncurredImcome(models.Model):
    MONTH_CHOICE = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
    )
    YEAR_CHOICE = (
        ('2023', '2023'),
        ('2024', '2024'),
        ('2025', '2025'),
        ('2026', '2026'),
        ('2027', '2027'),
       ('2028', '2028'),
        ('2029', '2029'),
       ('2030', '2030'),
        ('2031', '2031'),
         ('2032', '2032'),
    )
    member = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    created_at = models.DateTimeField(default=datetime.now, verbose_name="Ngày tạo")
    description = models.CharField(max_length=250, verbose_name='Mô tả')
    amount = models.FloatField(verbose_name="Số tiền")
    month_period =models.CharField(max_length=50, choices= MONTH_CHOICE, 
        verbose_name = 'Tháng chi lương')
    year_period =models.CharField(max_length=50, choices= YEAR_CHOICE, 
        verbose_name = 'Năm chi lương')
    class Meta:
        verbose_name = 'Khoản thu chi bất thường'
        verbose_name_plural = 'Khoản thu chi bất thường'
    

    
    def __str__(self):
        return self.member.username
    
    
