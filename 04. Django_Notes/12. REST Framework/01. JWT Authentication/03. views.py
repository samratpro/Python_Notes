from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from app.models import DataList
from api.serializers import DataListSerializers
from django.http import JsonResponse


# Login View
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = get_object_or_404(User, username=username)
        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    


# View to fetch data with query for authenticated users
class DataListView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        Query = request.headers.get('Query-Parameter')  # Extra parameter from 
        if not login_token:
            return JsonResponse({'error': 'Login token missing'}, status=400)
          
        Data_sites = DataList.objects.filter(Query=Query)
        if not Data_sites.exists():
            return JsonResponse({'error': 'No sites found for the given login token'}, status=404)
        serializer = DataListSerializers(user_automation_sites, many=True)
        
        return Response(serializer.data)
