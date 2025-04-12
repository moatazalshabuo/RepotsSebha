from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from .forms import *
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

CustomUser = get_user_model()

@login_required
def index(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    else:
        return redirect('subadmin_dashboard')
    return render(request,'index.html')

def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

@login_required
@superuser_required
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

@login_required
@superuser_required
def add_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CustomUserForm()
    return render(request, 'users/user_form.html', {'form': form, 'title': 'إضافة مستخدم'})

@login_required
@superuser_required
def edit_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CustomUserForm(instance=user)
    return render(request, 'users/user_form.html', {'form': form, 'title': 'تعديل المستخدم'})

@login_required
@superuser_required
def delete_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'users/user_confirm_delete.html', {'user': user})

@login_required
@superuser_required
def toggle_user_status(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    user.is_active = not user.is_active
    user.save()
    return redirect('user_list')

def get_ads_type_by_user_type(user_type):
    return {
        "traffic": 1,
        "ambulance": 2,
        "help": 3,
        "fire": 4,
    }.get(user_type, 0)

@login_required
def ads_list(request):
    if request.user.is_superuser:
        ads = Ads.objects.all()
    else:
        # نعرض فقط الإعلانات اللي نوعها نفس نوع المستخدم
        ads = Ads.objects.filter(type_ads=get_ads_type_by_user_type(request.user.type))
    return render(request, 'ads/ads_list.html', {'ads': ads})

@login_required
def add_ad(request):
    # الحد الأقصى للإعلانات المسموح بها
    MAX_ADS = 3

    # عدد الإعلانات التي نشرها المستخدم
    user_ads_count = Ads.objects.filter(type_ads=get_ads_type_by_user_type(request.user.type)).count()

    if user_ads_count >= MAX_ADS:
        messages.warning(request, "لقد وصلت إلى الحد الأقصى لعدد الإعلانات المسموح به (3 إعلانات).")
        return redirect('ads_list')

    if request.method == 'POST':
        form = AdsForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.publisher = request.user

            # تعيين نوع الإعلان حسب نوع المستخدم
            user_type = request.user.type
            if user_type == "traffic":
                ad.type_ads = 1
            elif user_type == "ambulance":
                ad.type_ads = 2
            elif user_type == "help":
                ad.type_ads = 3
            elif user_type == "fire":
                ad.type_ads = 4
            else:
                ad.type_ads = 0  # دارة التطبيق (افتراضي)

            ad.save()
            messages.success(request, "تمت إضافة الإعلان بنجاح.")
            return redirect('ads_list')
        else:
            messages.success(request, "خطاء .")
    else:
        form = AdsForm()

    return render(request, 'ads/ad_form.html', {'form': form, 'title': 'إضافة إعلان'})

@login_required
def edit_ad(request, pk):
    ad = get_object_or_404(Ads, pk=pk)
    if request.method == 'POST':
        form = AdsForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ads_list')
    else:
        form = AdsForm(instance=ad)
    return render(request, 'ads/ad_form.html', {'form': form, 'title': 'تعديل إعلان'})

@login_required
def delete_ad(request, pk):
    ad = get_object_or_404(Ads, pk=pk)
    if request.method == 'POST':
        ad.delete()
        return redirect('ads_list')
    return render(request, 'ads/ad_confirm_delete.html', {'ad': ad})

@login_required
def reports_list(request):
    # فلترة حسب نوع المستخدم
    user_type = request.user.type
    reports = Report.objects.filter(type=user_type)

    # فلترة حسب النوع والحالة (من GET)
    report_type = request.GET.get('type')
    status = request.GET.get('status')

    # if report_type:
    #     reports = reports.filter(type=report_type)
    if status:
        reports = reports.filter(status=status)

    # Pagination
    paginator = Paginator(reports, 10)  # 10 بلاغات في كل صفحة
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'filter_type': report_type,
        'filter_status': status
    }
    return render(request, 'reports/reports_list.html', context)

def report_detail(request, pk):
    report = get_object_or_404(Report, pk=pk)
    return render(request, 'reports/report_detail.html', {'report': report})

def update_report_status(request, pk, new_status):
    report = get_object_or_404(Report, pk=pk)

    # تحقّق من الطريقة (POST فقط)
    if request.method == 'POST':
        report.status = new_status
        report.save()
        messages.success(request, "تم تحديث حالة البلاغ بنجاح.")
        return redirect('report_detail', pk=pk)
def map_reports(request):
    return render(request,'reports/map_reports.html')

from django.db.models import Count

def admin_dashboard(request):
    User = get_user_model()

    users_count = User.objects.count()
    reports_count = Report.objects.count()
    ads_count = Ads.objects.count()
    resolved_count = Report.objects.filter(status=2).count()

    # بلاغات حسب النوع
    pie_data = Report.objects.values('type').annotate(total=Count('id'))
    pie_labels = [r['type'].capitalize() for r in pie_data]
    pie_values = [r['total'] for r in pie_data]

    # بلاغات حسب الحالة
    bar_data = [
        Report.objects.filter(status=0).count(),
        Report.objects.filter(status=1).count(),
        Report.objects.filter(status=2).count(),
    ]

    recent_users = User.objects.order_by('-last_login')[:10]

    context = {
        'users_count': users_count,
        'reports_count': reports_count,
        'ads_count': ads_count,
        'resolved_count': resolved_count,
        'pie_labels': pie_labels,
        'pie_data': pie_values,
        'bar_data': bar_data,
        'recent_users': recent_users
    }
    return render(request, 'dashboard/admin.html', context)

def authority_dashboard(request):
    user_type = request.user.type
    reports = Report.objects.filter(type=user_type)

    context = {
        'total_reports': reports.count(),
        'in_progress': reports.filter(status=1).count(),
        'resolved_reports': reports.filter(status=2).count(),
        'recent_reports': reports.order_by('-created_at')[:10],
    }
    return render(request, 'dashboard/subadmin.html', context)
