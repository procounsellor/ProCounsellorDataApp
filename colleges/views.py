from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EnggCollegeInfo
from .serializers import EnggCollegeInfoSerializer


# Create your views here.
class CollegeByNameAPIView(APIView):
    def get(self, request):
        college_name = request.query_params.get('name')
        if not college_name:
            return Response({"error": "Missing 'name' query parameter."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            college = EnggCollegeInfo.objects.get(name__iexact=college_name.strip())
            return Response(college.data, status=status.HTTP_200_OK)  # Only return JSONField `data`
        except EnggCollegeInfo.DoesNotExist:
            return Response({"error": f"No data found for '{college_name}'."}, status=status.HTTP_404_NOT_FOUND)