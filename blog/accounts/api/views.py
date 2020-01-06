from . import serializers
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model


User = get_user_model()


class UserCreateView(generics.CreateAPIView):
	serializer_class = serializers.UserCreateSerializer
	permission_classes = [AllowAny]
	queryset = User.objects.all()



