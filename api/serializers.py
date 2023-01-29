from master.models import (Province, District,
    LocalLevel, AppClient)
from authentication.models import User
from rest_framework import serializers

# class ComplaintSeveritySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ComplaintSeverity
#         fields = '__all__'
        
class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'
class DistrictSerializer(serializers.ModelSerializer):
    province = ProvinceSerializer(many=False)
    class Meta:
        model = District
        fields = '__all__'
class LocalLevelSerializer(serializers.ModelSerializer):
    district = DistrictSerializer(many=False)
    class Meta:
        model = LocalLevel
        fields = '__all__'


        # serializewrs with childs with in it i.e. nested serializer
# class DistrictSerializer(serializers.ModelSerializer):
#     local_levels = serializers.SerializerMethodField()
#     class Meta:
#         model = District
#         fields = '__all__'
#     def get_local_levels(self,obj):
#         local_levels = obj.locallevel_set.all()
#         serializer = LocalLevelSerializer(local_levels, many=True)
#         return serializer.data
# class ProvinceSerializer(serializers.ModelSerializer):
#     districts = serializers.SerializerMethodField()
#     class Meta:
#         model = Province
#         fields = '__all__'
#     def get_districts(self,obj):
#         districts = obj.district_set.all()
#         serializer = DistrictSerializer(districts, many=True)
#         return serializer.data
class AppClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppClient
        fields = '__all__'
# class ComplaintTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ComplaintType
#         fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'