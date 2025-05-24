from django.contrib import admin
from .models import CustomUser
# Register your models here.
# admin.site.register(CustomUser)
from .models import CustomUser, EmergencyCenter, Report, Attechment, Ads
admin.site.register(CustomUser)

admin.site.register(EmergencyCenter)

admin.site.register(Report)

admin.site.register(Attechment)

admin.site.register(Ads)
