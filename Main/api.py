from django.shortcuts import render
from .forms import *
from .serializers import *
from django.http import JsonResponse

from rest_framework.decorators import api_view,permission_classes,authentication_classes


@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def register_user(request):
    form = RegisterForm(request.data)
    if form.is_valid():
        user = CustomUser.objects.create(
            username=form.cleaned_data['phone'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
         
        )
        user.set_password(form.cleaned_data['password'])
        user.type = 'user'
        user.user_type = 'user'
        user.is_active = False
        user.save()

        # رجع البيانات باستخدام serializer
        serialized_user = UserSerializer(user)
        return JsonResponse(serialized_user.data, status=201)
    else:
        return JsonResponse(form.errors, status=400)


@api_view(['GET'])
@permission_classes([])
def me(request):
    user = request.user
    serialized_user = UserSerializer(user)
    return JsonResponse(serialized_user.data, status=201)


@api_view(['POST'])
@permission_classes([])
def create_report(request):
    print(request.user)
    if request.method == "POST":

        report_form = ReportForm(request.POST)
        if report_form.is_valid():

            report = report_form.save(commit=False)
            report.created_by = request.user
            report.save()  # حفظ البلاغ في قاعدة البيانات
            # التحقق مما إذا كانت هناك ملفات مرفقة
            files = request.FILES.getlist("files")  # استقبال ملفات متعددة
            for file in files:
                # t = AttechmentForm({'report_id':report.id},files={'file':file})
                # t.save()
                Attechment.objects.create(report=report, file=file)

            return JsonResponse({
                "message": "تم إنشاء البلاغ بنجاح",
                "report": {
                    "id": report.id,
                    "type": report.type,
                    "details": report.details,
                    "lng": report.lng,
                    "lat": report.lat,
                    "status": report.status,
                    "created_at": report.created_at,
                    "updated_at": report.updated_at,
                },
                "attachments": [file.file.url for file in report.attechment_set.all()]
            }, status=201)

        return JsonResponse({"errors": report_form.errors}, status=400)

    return JsonResponse({"errors": 'error'}, status=400)
# def report_list(request):
#     if not request.user.is_superuser:
#         reports = Report.objects.filter(type=request.user.type)
#     else:
#         reports = 

@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def create_ads(request):
    print(request.POST)
    USER_TYPE_TO_ADS_TYPE = {
    "traffic": 1,
    "ambulance": 2,
    "help": 3,
    "fire": 4,
    }
    if request.user.is_anonymous:
        anonymous_ads_form = AnonymousAdForm(request.POST,request.FILES)

        if anonymous_ads_form.is_valid():
            anonymous_ads_form.save()
            return JsonResponse({"message": "تم حفظ الإعلان بنجاح (مستخدم)."}, status=201)

        else:
            return JsonResponse({"errors": anonymous_ads_form.errors}, status=400)
    else:
        authenticated_ad_form = AuthenticatedAdForm(request.POST, request.FILES)

        if authenticated_ad_form.is_valid():
            ad_instance = authenticated_ad_form.save(commit=False)
            
            user_type = request.user.type
            type_ads = USER_TYPE_TO_ADS_TYPE[user_type]

            if type_ads is None:
                return JsonResponse({"error": "نوع المستخدم غير صالح أو غير معرف."}, status=400)

            ad_instance.type_ads = type_ads
            ad_instance.publisher = request.user
            ad_instance.save()

            return JsonResponse({"message": "تم حفظ الإعلان بنجاح (مستخدم)."}, status=201)

        else:
            return JsonResponse({"errors": authenticated_ad_form.errors}, status=400)

@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def get_ads(request):
    ads = Ads.objects.all()
    return JsonResponse(data=AdsSerializer(ads,many=True).data,safe=False)

@api_view(['GET'])
@permission_classes([])
def get_my_reports(request):
    # status = request.GET['status']
    reports = Report.objects.filter(created_by = request.user)
    # if request.GET['status']:
    #     reports = reports.filter(status=request.GET['status'])
    return JsonResponse(data=ReportSerializer(reports,many=True).data,safe=False)


@api_view(['GET'])
@permission_classes([])
def delete_report(requset,id):
    report = Report.objects.get(pk=id)
    report.status = 3
    report.save()
    return JsonResponse('تم الاغاء بنجاح',safe=False)
def reports_api(request):
    reports = Report.objects.filter(type=request.user.type,status=0).order_by('created_at')
    serializer = ReportSerializer(reports, many=True)
    return JsonResponse(serializer.data,safe=False)
# from geopy.distance import geodesic
# def nearest_centers_api(request):
#     report_type = request.GET.get("type")
#     lat = request.GET.get("lat")
#     lng = request.GET.get("lng")

#     if not (report_type and lat and lng):
#         return JsonResponse({"error": "Missing parameters"}, status=400)

#     centers = EmergencyCenter.objects.filter(type=report_type)
#     user_location = (float(lat), float(lng))

#     result = []
#     for center in centers:
#         center_location = (float(center.location_lat), float(center.location_lng))
#         distance_km = geodesic(user_location, center_location).km
#         result.append({
#             "id": center.id,
#             "name": center.name,
#             "distance": round(distance_km, 2)
#         })

#     # ترتيب حسب المسافة
#     result.sort(key=lambda x: x["distance"])
#     return JsonResponse(result, safe=False)

@api_view(['GET'])
@permission_classes([])
def emergency_centers_map(request):
    # مراكز بنفس نوع الجهة التابعة للمستخدم (مثلاً مرور)
    centers = EmergencyCenter.objects.filter()
    serializer = EmergencyCenterMapSerializer(centers, many=True)
    return JsonResponse(serializer.data,safe=False)