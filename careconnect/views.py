from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import (
    PatientDoctorMappingSerializer,
    PatientSerializer,
    DoctorSerializer,
    UserProfileSerializer,
)
from . import permissions  # Use relative import for permissions
from . import models  # Use relative import for models


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class PatientDoctorMappingViewSet(viewsets.ModelViewSet):
    queryset = PatientDoctorMapping.objects.all()
    serializer_class = PatientDoctorMappingSerializer

    # Custom endpoint to get all doctors for a specific patient
    @action(detail=True, methods=["get"], url_path="doctors")
    def doctors(self, request, pk=None):
        mappings = PatientDoctorMapping.objects.filter(patient_id=pk)
        doctors = [m.doctor for m in mappings]
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""

    serializer_class = UserProfileSerializer
    queryset = models.UserProfile.objects.all()  # Ensure this is correct
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "email"]


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
