from rest_framework.serializers import (
    CharField, 
    IntegerField, 
    Serializer,
    EmailField,
    ValidationError,
    JSONField,
    DateTimeField,
    ModelSerializer, 
    DictField, 
    ListField, 
    FloatField,
    )
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.conf import settings

CustomUser = get_user_model()
SUPERUSER_LIFE_TIME = timedelta(days=7)
DEFAULT_LIFE_TIME = timedelta(days=1)
TEST_LIFE_TIME = timedelta(hours=1)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    algorithm = 'RS256'

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['account_type'] = user.account_type

        if (user.is_superuser) or (user.is_staff) or (user.is_admin):
            token.access_token.set_exp(lifetime=SUPERUSER_LIFE_TIME) # token.access.set_exp(lifetime=SUPERUSER_LIFE_TIME) or token.set_exp(lifetime=exp)
            token['account_type'] = 'admin'
        else:
            if token['account_type'] in ['staging', 'production', 'developer']:
                token.access_token.set_exp(lifetime=DEFAULT_LIFE_TIME)
            elif token['account_type'] == 'test':
                token.access_token.set_exp(lifetime=TEST_LIFE_TIME) 

        token['uid'] = user.id

        return token

class UserCreateSerializer(Serializer):
    email = EmailField()
    username = CharField(max_length=150)
    password = CharField(write_only=True)
    account_type = CharField(max_length=50)
    token = CharField(write_only=True)

    def create(self, validated_data):
        account_type = validated_data.pop('account_type')
        password = validated_data.pop('password')
        email = validated_data.pop('email')

        if (account_type == 'developer') or (account_type == 'staging') or (account_type == 'production'):
            user = CustomUser.objects.create_staffuser(
                email=email,
                username=validated_data['username'],
                password=password
            )
        elif account_type == 'admin':
            user = CustomUser.objects.create_admin(
                email=email,
                username=validated_data['username'],
                password=password
            )
        elif account_type == 'superuser':
            user = CustomUser.objects.create_superuser(
                email=email,
                username=validated_data['username'],
                password=password
            )
        else:
            user = CustomUser.objects.create_user(
                email=email,
                username=validated_data['username'],
                password=password,
                account_type=account_type
            )

        return user

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise ValidationError('Email address is already in use')
        return value

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise ValidationError('Username is already in use')
        return value

    def validate_password(self, value):
        try:
            django_validate_password(value)
        except ValidationError as error:
            raise ValidationError({'password': error.messages})
    
    def validate_token(self, value):
        if value != settings.CREATE_USER_SECRET:
            raise ValidationError('Invalid token')
        return value

class SuccessResponseSerializer(Serializer):
    data = CharField()
    code = IntegerField()
    status = CharField()

class ErrorResponseSerializer(Serializer):
    message = CharField()
    code = IntegerField()
    status = CharField()
    error = CharField()