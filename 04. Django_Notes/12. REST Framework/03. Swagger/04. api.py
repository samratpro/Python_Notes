from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import (
    SoftwareSerializer, DeviceRegistrationSerializer
)
from .models import Software, Device
from django.utils import timezone
import re

# default
class SoftwareViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing software instances.
    """
    queryset = Software.objects.all()
    serializer_class = SoftwareSerializer
    permission_classes = [permissions.IsAdminUser]


# Customize

@swagger_auto_schema(
    method='post',
    operation_description="Verify user credentials, license, and register a device",
    manual_parameters=[
        openapi.Parameter('email', openapi.IN_PATH, 
            description="User's email address",
            type=openapi.TYPE_STRING,
            required=True),
        openapi.Parameter('password', openapi.IN_PATH,
            description="User's password",
            type=openapi.TYPE_STRING,
            required=True),
        openapi.Parameter('software_id', openapi.IN_PATH,
            description="Software ID",
            type=openapi.TYPE_INTEGER,
            required=True),
        openapi.Parameter('mac_address', openapi.IN_PATH,
            description="Device MAC address",
            type=openapi.TYPE_STRING,
            required=True)
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'device_name': openapi.Schema(type=openapi.TYPE_STRING, description="Device name", default="Unknown Device"),
            'device_type': openapi.Schema(type=openapi.TYPE_STRING, description="Device type", default="Unknown"),
            'os_version': openapi.Schema(type=openapi.TYPE_STRING, description="Operating system version", default="Unknown"),
            'ip_address': openapi.Schema(type=openapi.TYPE_STRING, description="Device IP address", default="0.0.0.0"),
            'location': openapi.Schema(type=openapi.TYPE_STRING, description="Device location", nullable=True)
        }
    ),
    responses={
        200: openapi.Response(
            description="Success",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING),
                    'data': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'plan_name': openapi.Schema(type=openapi.TYPE_STRING),
                            'plan_type': openapi.Schema(type=openapi.TYPE_STRING),
                            'credit_type': openapi.Schema(type=openapi.TYPE_STRING),
                            'remaining_credits': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                            'expiration_date': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
                            'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            'max_devices': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'active_devices': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'license_key': openapi.Schema(type=openapi.TYPE_STRING),
                            'device_id': openapi.Schema(type=openapi.TYPE_INTEGER)
                        }
                    )
                }
            )
        ),
        400: 'Bad Request - Invalid input data',
        401: 'Unauthorized - Invalid credentials',
        403: 'Forbidden - License expired or device limit reached',
        404: 'Not Found - Software or purchase not found',
        500: 'Internal Server Error'
    }
)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@csrf_exempt
def verify_license(request, email, password, software_id, mac_address):
    """
    Verify user credentials, license, and register a device.
    """
    try:
        logger.info(f"Starting license verification process...")
        logger.info(f"Input - Email: {email}, Software ID: {software_id}, MAC: {mac_address}")

        # Get optional parameters from request body
        device_name = request.data.get('device_name', 'Unknown Device')
        device_type = request.data.get('device_type', 'Unknown')
        os_version = request.data.get('os_version', 'Unknown')
        ip_address = request.data.get('ip_address', '0.0.0.0')
        location = request.data.get('location')

        # 1. Validate MAC address format
        if not re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', mac_address):
            return Response({
                'status': 'error',
                'message': 'Invalid MAC address format. Expected format: XX:XX:XX:XX:XX:XX'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 2. Authenticate user
        user = authenticate(request, username=email, password=password)
        if not user:
            logger.warning(f"Authentication failed for email: {email}")
            return Response({
                'status': 'error',
                'message': 'Invalid email or password'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        logger.info(f"User authenticated successfully: {user.id}")

        # 3. Check if software exists
        try:
            software = Software.objects.get(id=software_id)
            logger.info(f"Found software: {software.name} (ID: {software.id})")
        except Software.DoesNotExist:
            logger.error(f"Software with ID {software_id} not found")
            return Response({
                'status': 'error',
                'message': f'Software with ID {software_id} not found'
            }, status=status.HTTP_404_NOT_FOUND)

        # 4. Get all active purchases for this user and software
        purchases = SoftwarePurchase.objects.filter(
            user=user,
            software=software,
            is_active=True
        ).order_by('-purchase_date')

        # 5. Check if we have either purchases or user credits
        has_purchases = purchases.exists()
        has_user_credits = user.credits > 0
        
        if not has_purchases and not has_user_credits:
            logger.error(f"No active purchases or user credits found for user {user.id} and software {software_id}")
            return Response({
                'status': 'error',
                'message': 'No active purchases or user credits found for this software'
            }, status=status.HTTP_404_NOT_FOUND)

        # 6. Check if device already exists
        existing_device = Device.objects.filter(
            software=software,
            mac_address=mac_address
        ).first()

        if existing_device:
            # Update existing device information
            existing_device.device_name = device_name
            existing_device.device_type = device_type
            existing_device.os_version = os_version
            existing_device.ip_address = ip_address
            existing_device.location = location
            existing_device.is_active = True
            existing_device.save()
            logger.info(f"Updated existing device: {existing_device.id}")
        else:
            # Check device limit
            active_devices_count = Device.objects.filter(
                software=software,
                is_active=True
            ).count()

            if active_devices_count >= software.max_devices:
                return Response({
                    'status': 'error',
                    'message': f'Maximum device limit ({software.max_devices}) reached for this software'
                }, status=status.HTTP_403_FORBIDDEN)

            # Create new device
            existing_device = Device.objects.create(
                software=software,
                device_name=device_name,
                device_type=device_type,
                os_version=os_version,
                ip_address=ip_address,
                mac_address=mac_address,
                location=location
            )
            logger.info(f"Created new device: {existing_device.id}")

        # 7. Get credit information from all active purchases and user credits
        total_remaining_credits = user.credits  # Start with user credits
        total_credits_limit = 0
        total_credits_used = 0
        active_purchases = []

        for purchase in purchases:
            purchase.calculate_expiration()
            if purchase.is_active:
                remaining_credits = None
                if purchase.credit_limit is not None:
                    remaining_credits = purchase.credit_limit - (purchase.credits_used or 0)
                    total_remaining_credits += remaining_credits
                    total_credits_limit += purchase.credit_limit
                    total_credits_used += (purchase.credits_used or 0)

                active_purchases.append({
                    'purchase_id': purchase.id,
                    'plan_name': purchase.plan.name,
                    'plan_type': purchase.plan.plan_type,
                    'credit_type': purchase.plan.credit_type,
                    'remaining_credits': remaining_credits,
                    'credit_limit': purchase.credit_limit,
                    'credits_used': purchase.credits_used,
                    'expiration_date': purchase.expiration_date,
                    'purchase_date': purchase.purchase_date,
                    'license_key': purchase.license_key
                })

        # 8. Prepare response data
        response_data = {
            'status': 'success',
            'data': {
                'user_id': user.id,
                'device_id': existing_device.id,
                'device_status': 'existing' if existing_device else 'new',
                'software_name': software.name,
                'software_version': software.version,
                'max_devices': software.max_devices,
                'active_devices': Device.objects.filter(software=software, is_active=True).count(),
                'total_credits': {
                    'remaining': total_remaining_credits,
                    'limit': total_credits_limit,
                    'used': total_credits_used,
                    'user_credits': user.credits
                },
                'active_purchases': active_purchases,
                'has_access': True  # Explicitly show access is granted
            }
        }

        logger.info(f"Successfully processed license verification for device: {existing_device.id}")
        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        logger.exception(f"Error in verify_license: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
