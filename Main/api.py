from django.shortcuts import render
from .forms import *
from .serializers import *
from django.http import JsonResponse
# Create your views here.
from rest_framework.decorators import api_view,permission_classes,authentication_classes

@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def create_report(request):
    print(request.POST)
    if request.method == "POST":

        report_form = ReportForm(request.POST)
        if report_form.is_valid():

            report = report_form.save()  # حفظ البلاغ في قاعدة البيانات
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

 
def reports_api(request):
    reports = Report.objects.filter(type=request.user.type,status=0).order_by('created_at')
    serializer = ReportSerializer(reports, many=True)
    return JsonResponse(serializer.data,safe=False)