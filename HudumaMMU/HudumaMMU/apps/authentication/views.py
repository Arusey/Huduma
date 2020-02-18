from django.shortcuts import render
import jwt
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.http import HttpResponse
from .serializers import UserSerializer
from .models import User


class CreateUserAPIView(APIView):

    # permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginUser(APIView):
    def post(self, request, *args, **kwargs):
        if not request.data:
            return Response(
                {
                    'Error': 'Please provide an email and a password'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        email = request.data['email']
        password = request.data['password']

        try:
            user = User.objects.get(email=email, password=password)
        except User.DoesNotExist:
            return Response({
                "Error": "Invalid email or password"
            },
            status=status.HTTP_400_BAD_REQUEST
            )

        if user:
            payload = {
                'email': user.email,
                'password': user.password
            }
            response_details = {
                'token': jwt.encode(payload, settings.SECRET_KEY),
                'message': "You have been successfully logged in",
                'status': status.HTTP_200_OK
            }

            return Response(response_details, status=response_details['status'])


        else:
            return Response(
                {
                    "Error": "Invalid credentials"
                },
                status=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
