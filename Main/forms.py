from django import forms
from .models import *

class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, label="كلمة المرور")
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False, label="تأكيد كلمة المرور")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'type', 'is_active', 'is_superuser']

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