from rest_framework import serializers
from .models import Patient, Doctor, PatientDoctorMapping, UserProfile


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"


class PatientMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["id", "name"]


class DoctorMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ["id", "name", "specialization"]


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    doctor = DoctorMiniSerializer(read_only=True)
    patient = PatientMiniSerializer(read_only=True)

    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(), source="doctor", write_only=True
    )
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(), source="patient", write_only=True
    )

    class Meta:
        model = PatientDoctorMapping
        fields = ["id", "patient", "doctor", "patient_id", "doctor_id"]


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = UserProfile
        fields = ("id", "email", "name", "password")
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}}
        }

    def create(self, validated_data):
        """Create and return a new user"""
        user = UserProfile.objects.create_user(
            email=validated_data["email"],
            name=validated_data["name"],
            password=validated_data["password"],
        )
        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)

        return super().update(instance, validated_data)
