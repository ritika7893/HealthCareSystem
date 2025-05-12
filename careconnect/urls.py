from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PatientViewSet,
    DoctorViewSet,
    PatientDoctorMappingViewSet,
    UserLoginApiView,
    UserProfileViewSet,
)

router = DefaultRouter()
router.register(r"patients", PatientViewSet, basename="patient")

router.register(r"doctors", DoctorViewSet, basename="doctor")
router.register(r"mappings", PatientDoctorMappingViewSet, basename="mapping")
router.register("profiles", UserProfileViewSet)


urlpatterns = [
    path("api/", include(router.urls)),
    path("login/", UserLoginApiView.as_view()),
]
