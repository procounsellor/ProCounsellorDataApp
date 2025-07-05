# myapp/urls.py

from django.urls import path
from .views import CollegeByNameAPIView

urlpatterns = [
    path('college/', CollegeByNameAPIView.as_view(), name='college-by-name'),
]
