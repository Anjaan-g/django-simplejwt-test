from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

# Create your views here.


class LoginViewSet(TokenObtainPairView):
    permission_class = (AllowAny,)
    def post(self, request, *args, **kwargs):
        uuid=request.data.get('user_uuid')
        if not uuid:
            return Response({'message':"UUID not provided"},status=400)
        try:
            user = get_user_model().objects.get(user_uuid=uuid)
            data = MyTokenObtainPairSerializer.get_token(user=user)
            # print(user_data)
            return Response({'access_token':data}, status=status.HTTP_200_OK)
        
        except ObjectDoesNotExist:
            return Response({'message':"User Does not exists"},status=400)
        


    
