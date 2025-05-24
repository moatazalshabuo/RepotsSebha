from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__' 
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'type', 'details', 'lng', 'lat', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class AttechmentSerializer(serializers.ModelSerializer):
    report = ReportSerializer(read_only=True)
    class Meta:
        model = Attechment
        fields = ['id', 'report', 'file']
        read_only_fields = ['id']

class AdsSerializer(serializers.ModelSerializer):
    publisher = serializers.StringRelatedField(read_only=True)  # يعرض اسم المستخدم بدل ID

    class Meta:
        model = Ads
        fields = ['id', 'title', 'details', 'image', 'type_ads', 'publisher', 'created_at']
        read_only_fields = ['id', 'publisher', 'created_at']


from rest_framework import serializers
from .models import EmergencyCenter, CustomUser

class EmergencyCenterSerializer(serializers.ModelSerializer):
    admin = serializers.StringRelatedField(read_only=True)
    user_account = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = EmergencyCenter
        fields = [
            'id', 'name', 'location_lat', 'location_lng',
            'admin', 'user_account'
        ]
        read_only_fields = ['id', 'admin', 'user_account']
class EmergencyCenterMapSerializer(serializers.ModelSerializer):
    center_type = serializers.CharField(source='user_account.get_type_display', read_only=True)
    latitude = serializers.DecimalField(source='location_lat', max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(source='location_lng', max_digits=9, decimal_places=6)

    class Meta:
        model = EmergencyCenter
        fields = ['id', 'name', 'latitude', 'longitude', 'center_type']