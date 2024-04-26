

from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly 
from rest_framework import viewsets, pagination, filters
from . import models
from . serializers import SpecializationSerializer,DesignationSerializer,AvailableTimeSerializer, DoctorSerializer, ReviewSerializer
# Create your views here.

class SpecializationViewset(viewsets.ModelViewSet):
    queryset = models.Specialization.objects.all()
    serializer_class = SpecializationSerializer


class DesignationViewset(viewsets.ModelViewSet):
    queryset = models.Designation.objects.all()
    serializer_class = DesignationSerializer


class AvailableTimeForSpecificDoctor(filters.BaseFilterBackend):
    def filter_queryset(self, request, query_set, view):
        doctor_id = request.query_params.get("doctor_id")
        if doctor_id:
            # jehetu doctor er sathe available_time er m2m relationship so amra doctor=doctor_id diye doctor k filter korte parbo ekhane doctor actually doctor model k indicate kore
            return query_set.filter(doctor = doctor_id)
        return query_set


# @permission_classes([IsAuthenticated]
class AvailableTimeViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly ]
    queryset = models.AvailableTime.objects.all()
    serializer_class = AvailableTimeSerializer
    filter_backends = [AvailableTimeForSpecificDoctor]


class DoctorPagination(pagination.PageNumberPagination):
    page_size = 1 #item per page
    page_size_query_param = page_size
    max_page_size = 100


class DoctorViewset(viewsets.ModelViewSet):
    queryset = models.Doctor.objects.all()
    serializer_class = DoctorSerializer
    pagination_class = DoctorPagination


class ReviewViewset(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = models.Review.objects.all()
    serializer_class = ReviewSerializer


