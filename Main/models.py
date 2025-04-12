from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    REPORT_TYPE_CHOICES = [
        ("traffic", "المرور"),     # بلاغ مروري
        ("help", "النجدة"),           # طلب مساعدة
        ("ambulance", "الاسعاف"),
         ('fire','المطافئ') # طلب إسعاف
    ]
    type = models.CharField(choices=REPORT_TYPE_CHOICES,max_length=50)
    def __str__(self):
        return self.email
    
class Report(models.Model):
    # تعريف أنواع البلاغات كخيارات ثابتة
    REPORT_TYPE_CHOICES = [
        ("traffic", "بلاغ مروري"),     # بلاغ مروري
        ("help", "بلاغ نجدة"),           # طلب مساعدة
        ("ambulance", "بلاغ اسعاف"), 
        ('fire','بلاغ مطافئ') # طلب إسعاف
    ]

    REPORT_STATUS_CHOICES = [
        (0, "New"),          # جديد
        (1, "In Progress"),  # قيد التنفيذ
        (2, "Resolved"),     # تم الحل
    ]

    type = models.CharField(
        max_length=20,
        choices=REPORT_TYPE_CHOICES,  # ربط الحقل بالخيارات المتاحة
        verbose_name="نوع البلاغ"
    )
    details = models.TextField(null=True, blank=True, verbose_name="تفاصيل البلاغ")
    lng = models.CharField(max_length=50, verbose_name="خط الطول")
    lat = models.CharField(max_length=50, verbose_name="خط العرض")
    status = models.IntegerField(
        blank=True,
        default=0,
        verbose_name="حالة البلاغ"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخر تحديث")

    def __str__(self):
        return f"{self.get_type_display()} - {self.get_status_display()}"

    class Meta:
        verbose_name = "بلاغ"
        verbose_name_plural = "البلاغات"
        ordering = ["-created_at"]

class Attechment(models.Model):
    report = models.ForeignKey(Report,on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')


class Ads(models.Model):
    ADS_TYPE_CHOICES = (
        (0, 'دارة التطبيق'),
        (1, 'مرور'),
        (2, 'الإسعاف'),
        (3, 'النجدة'),
        (4, 'المطافئ'),
    )

    title = models.CharField(max_length=255, verbose_name="عنوان الإعلان")
    details = models.TextField(null=True, blank=True, verbose_name="تفاصيل الإعلان")
    image = models.FileField(upload_to='ads/', null=True, blank=True, verbose_name="صورة الإعلان")
    type_ads = models.IntegerField(choices=ADS_TYPE_CHOICES,null=True,blank=True, verbose_name="نوع الإعلان")
    publisher = models.ForeignKey('CustomUser', on_delete=models.CASCADE,null=True,blank=True,verbose_name="الناشر")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")
    class Meta:
        ordering = ["-created_at"]