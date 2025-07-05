
from .models import EnggCollegeInfo
from rest_framework import serializers

class EnggCollegeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnggCollegeInfo
        field = '__all__'