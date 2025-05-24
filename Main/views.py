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
        if request.user.type == 'emergency_admin':
            return redirect('subadmin_dashboard')
        else:
            return redirect('center_dashboard')

def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

@login_required
@superuser_required
def user_list(request):
    """
    عرض قائمة المستخدمين مع دعم الفلاتر والبحث
    """
    # الحصول على جميع المستخدمين بشكل أساسي
    users = CustomUser.objects.all().order_by('username')
    
    # إعداد نموذج الفلتر
    filter_form = UserFilterForm(request.GET or None)
    
    # تطبيق الفلاتر إذا تم تقديم النموذج
    if filter_form.is_valid():
        # فلتر حسب الحالة
        status = filter_form.cleaned_data.get('status')
        if status == 'active':
            users = users.filter(is_active=True)
        elif status == 'inactive':
            users = users.filter(is_active=False)
        
        # فلتر حسب النوع
        user_type = filter_form.cleaned_data.get('type')
        if user_type:
            users = users.filter(type=user_type)
        
        # البحث
        search_query = filter_form.cleaned_data.get('search')
        if search_query:
            users = users.filter(
                Q(username__icontains=search_query) | 
                Q(email__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
            )
    
    # الحصول على خيارات النوع للقائمة المنسدلة
    type_choices = CustomUser._meta.get_field('type').choices
    # users = CustomUser.objects.all()
    return render(request, 'users/user_list.html', {'users': users,'filter_form': filter_form,
        'type_choices': type_choices,
        'active_count': CustomUser.objects.filter(is_active=True).count(),
        'inactive_count': CustomUser.objects.filter(is_active=False).count(),
        'superuser_count': CustomUser.objects.filter(is_superuser=True).count(),})

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
from geopy.distance import geodesic
def report_detail(request, pk):
    report = get_object_or_404(Report, pk=pk)
    report_location = (float(report.lat), float(report.lng))

    # المراكز من نفس نوع البلاغ
    centers = EmergencyCenter.objects.filter(type=report.type)

    # نحسب المسافة لكل مركز
    center_data = []
    for center in centers:
        distance_km = geodesic(report_location, (float(center.location_lat), float(center.location_lng))).km
        center_data.append({
            'id': center.id,
            'name': center.name,
            'lat': float(center.location_lat),
            'lng': float(center.location_lng),
            'distance': round(distance_km, 2),
        })

    # ترتيب حسب الأقرب
    center_data.sort(key=lambda x: x['distance'])

    return render(request, 'reports/report_detail.html', {
        'report': report,
        'centers': center_data
    })

def update_report_status(request, pk, new_status):
    report = get_object_or_404(Report, pk=pk)

    if request.method == 'POST':
        report.status = new_status

        # إذا تم إرسال center_id من الفورم
        center_id = request.POST.get('center_id')
        if center_id:
            try:
                center = EmergencyCenter.objects.get(pk=center_id)
                report.assigned_center = center
            except EmergencyCenter.DoesNotExist:
                messages.warning(request, "المركز المحدد غير موجود.")

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

from .models import EmergencyCenter

def authority_dashboard(request):
    user_type = request.user.type  # مثلاً: 'ambulance'
    reports = Report.objects.filter(type=user_type)
    centers = EmergencyCenter.objects.filter(user_account__type=user_type)
    for center in centers:
        if center.user_account.type == 'traffic':
            center.icon = '🚓'
        elif center.user_account.type == 'ambulance':
            center.icon = '🚑'
        elif center.user_account.type == 'help':
            center.icon = '🛟'
        elif center.user_account.type == 'fire':
            center.icon = '🔥'
        else:
            center.icon = '📍'
    context = {
        'total_reports': reports.count(),
        'in_progress': reports.filter(status=1).count(),
        'resolved_reports': reports.filter(status=2).count(),
        'recent_reports': reports.order_by('-created_at')[:10],
        'centers': centers,  # ← تمرير مراكز الطوارئ
    }
    return render(request, 'dashboard/subadmin.html', context)

@login_required
def create_emergency_center(request):
    if request.method == 'POST':
        user_form = EmergencyCenterUserForm(request.POST)
        center_form = EmergencyCenterForm(request.POST)

        if user_form.is_valid() and center_form.is_valid():
            # حفظ المستخدم
            user = user_form.save(commit=False)
            user.user_type = 'emergency_center'
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            # حفظ بيانات المركز وربطه بالمستخدم الذي أنشأه كمشرف (emergency_admin)
            center = center_form.save(commit=False)
            center.user_account = user
            if request.user.user_type == 'emergency_admin':
                center.admin = request.user
            center.type = request.user.type
            center.save()

            return redirect('center_list')  # غيّرها لمسار العرض المناسب
    else:
        user_form = EmergencyCenterUserForm()
        center_form = EmergencyCenterForm()

    return render(request, 'center/add.html', {
        'user_form': user_form,
        'center_form': center_form
    })
@login_required
def center_list(request):
    if request.user.user_type == 'emergency_admin':
        # فقط المراكز التابعة للمشرف الحالي
        centers = EmergencyCenter.objects.filter(type=request.user.type)
    else:
        # كل المراكز (للمدير العام مثلاً)
        centers = EmergencyCenter.objects.all()

    return render(request, 'center/list.html', {
        'centers': centers
    })
@login_required
def edit_emergency_center(request, center_id):
    center = get_object_or_404(EmergencyCenter, id=center_id)
    user = center.user_account

    if request.method == 'POST':
        user_form = EmergencyCenterUserForm(request.POST, instance=user)
        center_form = EmergencyCenterForm(request.POST, instance=center)

        if user_form.is_valid() and center_form.is_valid():
            # حفظ الحساب
            user_form.save()
            # حفظ المركز
            center_form.save()
            return redirect('center_list')
    else:
        user_form = EmergencyCenterUserForm(instance=user)
        center_form = EmergencyCenterForm(instance=center)

    return render(request, 'center/add.html', {
        'user_form': user_form,
        'center_form': center_form,
        'edit_mode': True,
        'center': center
    })

@login_required
def delete_emergency_center(request, center_id):
    center = get_object_or_404(EmergencyCenter, id=center_id)

    # حذف الحساب المرتبط (user_account)
    if center.user_account:
        center.user_account.delete()

    # سيتم حذف المركز تلقائيًا بعد حذف الـ OneToOne user_account بسبب العلاقة
    center.delete()

    return redirect('center_list')

# from django.contrib.auth.decorators import login_required
# from django.core.paginator import Paginator
# from django.shortcuts import render
from django.db.models import Q
# from .models import Report

def center_reports(request):
    user = request.user

    # التحقق من أن المستخدم هو مشرف طوارئ ولديه مركز على الأقل
    centers = EmergencyCenter.objects.filter(admin=user)
    if not centers.exists():
        return render(request, '403.html')  # ليس مشرف على أي مركز

    # جلب كل البلاغات المرتبطة بالمراكز التي يشرف عليها المستخدم
    reports = Report.objects.filter(assigned_center__in=centers)

    # فلترة حسب الحالة - الافتراضي هو 'قيد التنفيذ' (status=1)
    status = request.GET.get('status', '1')
    if status in ['0', '1', '2', '3']:
        reports = reports.filter(status=int(status))

    # فلترة حسب البحث
    search = request.GET.get('search')
    if search:
        reports = reports.filter(
            Q(details__icontains=search) |
            Q(created_by__username__icontains=search)
        )

    reports = reports.order_by('created_at')

    # تقسيم الصفحات
    paginator = Paginator(reports, 10)
    page_number = request.GET.get('page')
    reports_page = paginator.get_page(page_number)

    return render(request, 'center/center_reports.html', {
        'reports': reports_page,
        'active_status': int(status),  # لإظهار الزر المختار في الفلاتر إن وجدت
        'search_query': search
    })


@login_required
def center_report_detail(request, pk):
    report = get_object_or_404(Report, pk=pk)

    # التأكد من أن المستخدم يشرف على المركز المرتبط بالبلاغ
    if report.assigned_center is None or report.assigned_center.admin != request.user:
        return render(request, '403.html')

    attachments = Attechment.objects.filter(report=report)
    return render(request, 'center/center_report_detail.html', {
        'report': report,
        'attachments': attachments
    })


@login_required
def center_update_report_status(request, pk):
    report = get_object_or_404(Report, pk=pk)

    # تحقق أن المشرف هو المسؤول عن المركز المعين
    if report.assigned_center is None or report.assigned_center.admin != request.user:
        return render(request, '403.html')

    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        if new_status in ['1', '2']:  # فقط تنفيذ أو تم الحل
            report.status = int(new_status)
            report.save()
            messages.success(request, "تم تحديث حالة البلاغ.")
        else:
            messages.error(request, "نوع الحالة غير صالح.")

    return redirect('center_report_detail', pk=pk)
from django.db.models.functions import ExtractHour

@login_required
def center_dashboard(request):
    user = request.user
    centers = EmergencyCenter.objects.filter(admin=user)

    if not centers.exists():
        return render(request, '403.html')

    reports = Report.objects.filter(assigned_center__in=centers)

    total_reports = reports.count()
    in_progress = reports.filter(status=1).count()
    resolved = reports.filter(status=2).count()

    # توزيع البلاغات حسب الساعة
    time_data = reports.annotate(hour=ExtractHour('created_at')) \
                       .values('hour') \
                       .annotate(count=Count('id')) \
                       .order_by('hour')

    hours = [f"{entry['hour']}:00" for entry in time_data]
    counts = [entry['count'] for entry in time_data]

    # أقدم 5 بلاغات قيد التنفيذ
    oldest_in_progress = reports.filter(status=1).order_by('created_at')[:5]

    return render(request, 'dashboard/center_dashboard.html', {
        'total_reports': total_reports,
        'in_progress': in_progress,
        'resolved': resolved,
        'hours': hours,
        'counts': counts,
        'map_reports': oldest_in_progress,
    })