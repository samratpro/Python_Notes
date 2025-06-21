from rest_framework import serializers
from .models import Software

# Default

class SoftwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Software
        fields = '__all__'

# Customize
class DeviceRegistrationSerializer(serializers.Serializer):
    email = serializers.CharField(
        max_length=254,
        required=True,
        allow_blank=False,
        allow_null=False,
        label='Email',
        help_text='User email address'
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        allow_blank=False,
        allow_null=False,
        label='Password',
        help_text='User password',
        style={'input_type': 'password'}
    )
    software_id = serializers.IntegerField(
        required=True,
        label='Software ID',
        help_text='ID of the software',
        min_value=1
    )
    device_info = serializers.DictField(
        required=True,
        allow_null=False,
        help_text='Device information (e.g., mac_address, device_name, device_type, os_version, ip_address, location)'
    )

    def validate_device_info(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("device_info must be a dictionary")
        if 'mac_address' not in value or not value['mac_address']:
            raise serializers.ValidationError("device_info must include a non-empty mac_address")
        return value

    def validate(self, data):
        return data
