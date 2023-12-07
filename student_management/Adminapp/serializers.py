# serializers.py rest_framework 
from rest_framework  import serializers
from Adminapp.models import StaffModel

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffModel
        fields = '__all__'
