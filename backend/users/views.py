from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import csv

from .models import CustomUser
from .serializers import UserSerializer


@api_view(['POST'])
def login_user(request):
    """Login a user by Facebook ID."""
    facebook_id = request.data.get('facebook_id')
    if not facebook_id:
        return Response({'error': 'Facebook ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = CustomUser.objects.get(facebook_id=facebook_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found. Please register first.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def register_user(request):
    """Register a new user with Facebook ID, full name, and email."""
    full_name = request.data.get('full_name')
    email = request.data.get('email')
    facebook_id = request.data.get('facebook_id')

    # Validate required fields
    if not all([full_name, email, facebook_id]):
        return Response({'error': 'Full name, email, and Facebook ID are required.'},
                        status=status.HTTP_400_BAD_REQUEST)
    
    # Check if user already exists
    if CustomUser.objects.filter(facebook_id=facebook_id).exists():
        return Response({'error': 'User already exists.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Create new user
    user = CustomUser.objects.create(full_name=full_name, email=email, facebook_id=facebook_id)
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def current_user(request):
    """Fetch current user by Facebook ID."""
    facebook_id = request.query_params.get('facebook_id')
    if not facebook_id:
        return Response({'error': 'Facebook ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = CustomUser.objects.get(facebook_id=facebook_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def export_users(request):
    """Export all users to CSV for Excel."""
    users = CustomUser.objects.all()
    serializer = UserSerializer(users, many=True)

    # Create HTTP response with CSV content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    # CSV header
    writer.writerow(['Facebook ID', 'Full Name', 'Email'])

    # CSV rows
    for user in serializer.data:
        writer.writerow([user['facebook_id'], user['full_name'], user['email']])

    return response
