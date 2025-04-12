from rest_framework import serializers
from .models import *

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