from django import forms
from .models import *

class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, label="كلمة المرور")
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False, label="تأكيد كلمة المرور")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'user_type', 'type', 'is_active', 'is_superuser']
        labels = {
            'username': 'اسم المستخدم',
            'email': 'البريد الإلكتروني',
            'first_name': 'الاسم الأول',
            'last_name': 'اسم العائلة',
            'user_type': 'نوع الحساب',
            'type': 'الجهة/القسم',
            'is_active': 'نشط؟',
            'is_superuser': 'مشرف عام؟',
        }
        widgets = {
            'user_type': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password or confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("كلمة المرور غير متطابقة")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=15, label='Phone Number')
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        phone = cleaned_data.get('phone')
        if CustomUser.objects.filter(username=phone).exists():
            raise forms.ValidationError("Phone number already registered.")

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['type', 'details', 'lng', 'lat', 'status']
        labels = {
            'type': 'نوع البلاغ',
            'details': 'تفاصيل البلاغ',
            'lng': 'خط الطول',
            'lat': 'خط العرض',
            'status': 'حالة البلاغ',
        }
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'lng': forms.TextInput(attrs={'class': 'form-control'}),
            'lat': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class AttechmentForm(forms.ModelForm):
    class Meta:
        model = Attechment
        fields = ['file']
        labels = {
            'file': 'إرفاق ملف',
        }
        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


# ✅ النموذج الأول: للزوار (يملأ الناشر ونوع الإعلان يدويًا)
class AnonymousAdForm(forms.ModelForm):
    class Meta:
        model = Ads
        fields = ['title', 'details', 'image', 'type_ads']


# ✅ النموذج الثاني: للمستخدمين المسجلين (ما فيش type_ads ولا publisher)
class AuthenticatedAdForm(forms.ModelForm):
    class Meta:
        model = Ads
        fields = ['title', 'details', 'image']

class AdsForm(forms.ModelForm):
    class Meta:
        model = Ads
        fields = ['title', 'details', 'image', 'type_ads']

class EmergencyCenterUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="كلمة المرور")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="تأكيد كلمة المرور")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'type']
        labels = {
            'username': 'اسم المستخدم',
            'email': 'البريد الإلكتروني',
            'first_name': 'الاسم الأول',
            'last_name': 'اسم العائلة',
            'type': 'الجهة/القسم (مرور، إسعاف...)'
        }
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("كلمة المرور غير متطابقة.")
        return cleaned_data


class EmergencyCenterForm(forms.ModelForm):
    class Meta:
        model = EmergencyCenter
        fields = ['name', 'location_lat', 'location_lng']
        labels = {
            'name': 'اسم المركز',
            'location_lat': 'خط العرض',
            'location_lng': 'خط الطول',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location_lat': forms.NumberInput(attrs={'class': 'form-control'}),
            'location_lng': forms.NumberInput(attrs={'class': 'form-control'}),
            }

class UserFilterForm(forms.Form):
    """
    نموذج فلترة المستخدمين في صفحة قائمة المستخدمين
    """
    STATUS_CHOICES = (
        ('', 'جميع الحالات'),
        ('active', 'مفعل'),
        ('inactive', 'موقوف'),
    )
    
    search = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'بحث عن مستخدم...',
            'autofocus': True,
        })
    )
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES, 
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )
    
    type = forms.ChoiceField(
        choices=(), 
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # إضافة خيارات النوع من النموذج ديناميكياً
        self.fields['type'].choices = [('', 'جميع الأنواع')] + list(CustomUser._meta.get_field('type').choices)