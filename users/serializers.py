import os
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# from fintech.utils import compress
# from rest_auth.registration.serializers import RegisterSerializer
# from rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer
from rest_framework import exceptions
from .models import CustomUser
from django.utils.translation import ugettext as _
from django.db.models import ObjectDoesNotExist
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login



class UserSerializer(serializers.ModelSerializer):
    username = None
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, write_only=True, required=True)
    phone_no = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'user_uuid', 'first_name', 'last_name', 'email', 'phone_no','role',
                 'is_superuser', 'is_admin',
                  'password', )
        lookup_field = 'email'
        # write_only_fields = ('password')
        read_only_fields = (
        'id', 'is_superuser', 'avatar', 'is_admin')

    def get_queryset(self):
        if self.request.user.is_staff:
            return CustomUser.objects.all()
        else:
            return self.request.user

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_no=validated_data['phone_no'],
            user_uuid=validated_data['user_uuid']

        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def create_admin(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_no=validated_data['phone_no'],
            is_admin=True,
            is_staff=True
        )
        user.set_password(validated_data['password'])
        user.save()
        return user



class AdminSerializer(serializers.ModelSerializer):
    username = None
    email = serializers.EmailField(required=True)

    # password1 = serializers.CharField(
    #     write_only=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ('id', 'user_uuid', 'first_name', 'last_name', 'role', 'email', 'phone_no', 'is_superuser', 'is_admin',
                  'password')
        lookup_field = 'email'
        write_only_fields = ('password')
        read_only_fields = (
            'id', 'user_uuid', 'is_superuser', 'is_admin'
        )

    @method_decorator(login_required())
    def create_admin(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_no=validated_data['phone_no'],
            is_admin=True,

        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomTokenSerializer(TokenObtainSerializer):
   
    def __init__(self, *args, **kwargs):
        self.fields['user_uuid'] = serializers.CharField()
    
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)
        # print(data)
        # self.user = authenticate(**authenticate_kwargs)
        try:
            self.user = CustomUser.objects.get(user_uuid=data['user_uuid'])
        except ObjectDoesNotExist:
            return 'User with provided UUID does not exist !!!'
        print(self.user) # --> None
        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        print(data)
        return data
    
    
class MyTokenObtainPairSerializer(CustomTokenSerializer):
    @classmethod
    def get_token(cls, user):
        # email = user.email
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['phone_no'] = user.phone_no
        token['role'] = user.role
        token['uuid'] = user.user_uuid
        print(token.access_token)
        return str(token.access_token)


# class LoginSerializer(LoginSerializer):
#     username = None
#     email = serializers.EmailField(required=True)
#     password = serializers.CharField(style={'input_type': 'password'})

#     def get_cleaned_data(self):
#         super(LoginSerializer, self).get_cleaned_data()
#         token = TokenObtainPairSerializer.get_token()
#         return token


class EditUserSerializer(serializers.ModelSerializer):
    username = None
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = (
            'id', 'first_name', 'last_name', 'email', 'phone_no', 'avatar', 'avatar_url',
            'is_superuser', 'is_admin'
        )
        lookup_field = 'email'
        # write_only_fields = ('password')
        read_only_fields = (
            'id', 'is_superuser', 'avatar_url', 'is_admin'
        )


class ReadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
        'id', 'first_name', 'last_name', 'role', 'user_uuid', 'email', 'phone_no', 'avatar_url',
        'is_superuser', 'is_admin')
        lookup_field = 'email'
        read_only_fields = (
        'id', 'first_name', 'last_name', 'role', 'user_uuid', 'email', 'phone_no', 'avatar_url',
        'is_superuser', 'is_admin')
