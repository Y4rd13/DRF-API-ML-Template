# Path for utils
from pathlib import Path
import sys

path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
path = path.replace('/myproject', '')
sys.path.insert(0, path)

# rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.views import TokenRefreshView

# drf_yasg (swagger) and django rest framework
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate, get_user_model

CustomUser = get_user_model()

# ClassificationGetResponseSerializer,
from .serializers import (
    SuccessResponseSerializer,
    ErrorResponseSerializer,
    CustomTokenObtainPairSerializer,
    UserCreateSerializer,
    MyCustomSerializer,
)

# Services, utils and tasks
import myapp.services as services
import myapp.tasks as tasks
from myproject.utils import handle_error


SuccessResponseSerializer = openapi.Response(
    description='Success in request', schema=SuccessResponseSerializer)
ErrorResponseSerializer = openapi.Response(
    description='Error on request', schema=ErrorResponseSerializer)


class MyCustomView(APIView):
    #throttle_scope = "myapp" # This is for throttling (see settings.py)
    serializer_class = MyCustomSerializer
    
    @swagger_auto_schema(
        request_body=serializer_class,
        operation_description='My Custom Service.',
        responses={HTTP_200_OK: SuccessResponseSerializer,
                     HTTP_400_BAD_REQUEST: ErrorResponseSerializer}
    )
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            my_variable = serializer.validated_data['my_variable']
            
            data = tasks.my_task_service.delay(x=my_variable)
            data = data.get()

            return Response(
                data = data,
                status=HTTP_200_OK
            )

        except Exception as e:
            return handle_error(e)

    @swagger_auto_schema(
        operation_description='Get some info.',
        manual_parameters=[
            openapi.Parameter('manual_variable', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        ],
        responses={
            HTTP_200_OK: SuccessResponseSerializer,
            HTTP_400_BAD_REQUEST: 'Invalid manual_variable.'
        }
    )
    def get(self, request):
        manual_variable = request.GET.get('manual_variable', None)

        try:
            return Response(
                data=f'Hello world: {manual_variable}',
                status=HTTP_200_OK
            )
        except Exception as e:
            return handle_error(e)

class UserCreate(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserCreateSerializer

    @swagger_auto_schema(
        request_body=serializer_class,
        operation_description='Create a new user account.',
        responses={HTTP_200_OK: SuccessResponseSerializer,
                   HTTP_400_BAD_REQUEST: ErrorResponseSerializer}
    )
    def post(self, request, format=None):
        serializer = UserCreateSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            validated_data['password'] = request.data.get('password')
            validated_data['token'] = request.data.get('token')
            user = serializer.create(validated_data)
            #user = serializer.save()
            #user.save()
            response_data = {
                'status': 'success',
                'message': 'User account created successfully',
                'account_type': user.account_type,
            }
            return Response(
                data=response_data,
                status=HTTP_201_CREATED
            )
        else:
            return Response(
                data=serializer.errors,
                status=HTTP_400_BAD_REQUEST
            )


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user_is_authenticated = authenticate(username=username, password=password)
        if user_is_authenticated:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                jwt_tokens = login_serializer.validated_data
                return Response(data=jwt_tokens, status=HTTP_200_OK)
        else:
            return Response(data={'message': 'Invalid username/password', 'code': HTTP_400_BAD_REQUEST, 'status': 'error'}, status=HTTP_400_BAD_REQUEST)

class CustomTokenRefreshView(TokenRefreshView):
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)

        access_token = serializer.validated_data['access']
        response_data = {
            'access': str(access_token),
        }
        return Response(data=response_data, status=HTTP_200_OK)


# Test view!
# Comment for production
from .tasks import *
class TestView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        # add any task here
        return Response(data={"status": True}, status=HTTP_200_OK)